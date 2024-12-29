import sys
sys.path.append("../..")
from utils.exception import MyError
import ast
from collections import defaultdict
from utils.data_preprocessing.employee_growth_per_quater_per_domain import calculate_percent_increase_in_employee_count
from constants.schema.emp_growth_per_quater_per_domain_fields import TENANT_ID , DOMAIN_NAME, QUATER, PERCENT_INCREASE
from constants import constants
from domains.new_dev_project.domain_infrastructure.initial_data_impl import InitialData
def convert_to_dict(value):
        try:
            # Try to convert string representation of a dictionary to a Python dictionary
            return ast.literal_eval(value)
        except Exception as e:
            # Raise custom error if conversion fails
            raise MyError(error_code=400, error_message="Cannot process data, input file type not supported yet!")
        

def group_by_year_and_role(data):
    grouped_data = defaultdict(lambda: defaultdict(dict))

# Process the input data
    for key, roles in data.items():
        year, month = key.split('-')  # Extract year and month
        month = int(month)  # Convert month to an integer
        
        for role, count in roles.items():
            # Group by year, role, and month
            grouped_data[role][year][month] = count

    # Convert defaultdict to a regular dictionary for display
    return dict(grouped_data)
    


def initial_data_for_emp_growth_per_role_per_quater_per_domain():
    df = InitialData.get_instance().get_data()
    selected_columns = df[['domain_name', 'employee_count_by_month_by_role']]
    selected_columns=selected_columns.dropna(subset=['domain_name', 'employee_count_by_month_by_role'])
    selected_columns['employee_count_by_month_by_role'] = selected_columns['employee_count_by_month_by_role'].apply(convert_to_dict).apply(group_by_year_and_role)
    return selected_columns


def calculate_percent_increase_in_employee_count_per_role_per_quater(grouped_employee_count_by_month_by_role):
    percent_increase_by_group=defaultdict(dict)
    for role,grouped_role_date in grouped_employee_count_by_month_by_role.items():
        percent_increase_by_group[role]=percent_increase_by_group[role]|calculate_percent_increase_in_employee_count(grouped_role_date)
    return percent_increase_by_group

def processed_data():
    intial_data=initial_data_for_emp_growth_per_role_per_quater_per_domain()
    final_data_to_return=[]
    for i in range(len(intial_data)):
        row=intial_data.iloc[i]
        domain_name=row['domain_name']
        grouped_employee_count_by_month=row['employee_count_by_month_by_role']  
        percent_increase_in_employee_count_per_quater_for_current_domain=calculate_percent_increase_in_employee_count_per_role_per_quater(grouped_employee_count_by_month)  
        for role,percent_increase_in_employee_count_per_quater in percent_increase_in_employee_count_per_quater_for_current_domain.items():
            for quater,percent_increase_in_employee_count in percent_increase_in_employee_count_per_quater.items():
                final_data_to_return.append({TENANT_ID:constants.TENANT_ID,"role":role,DOMAIN_NAME:domain_name,QUATER:quater,PERCENT_INCREASE:percent_increase_in_employee_count})
    return final_data_to_return

