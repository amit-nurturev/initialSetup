import sys
sys.path.append("../..")
import ast
import pandas as pd
from constants import constants
from utils.exception import *
from collections import defaultdict
from constants.schema.emp_growth_per_quater_per_domain_fields import TENANT_ID , DOMAIN_NAME, QUATER, PERCENT_INCREASE
from domains.new_dev_project.domain_infrastructure.initial_data_impl import InitialData


def convert_to_dict(value):
        try:
            # Try to convert string representation of a dictionary to a Python dictionary
            return ast.literal_eval(value)
        except Exception as e:
            # Raise custom error if conversion fails
            raise MyError(error_code=400, error_message="Cannot process data, input file type not supported yet!")
        


# Function to group the employee count by year and month
def group_by_year(value):
    # Create a defaultdict to store the counts by year
    grouped_data = defaultdict(dict)
    
    # Iterate through the months and counts in the given dictionary
    for month_year, count in value.items():
        # Extract year and month from the key
        year, month = month_year.split('-')
        year = int(year)  # Convert year to integer
        month = int(month)  # Convert month to integer
        
        # Group the data by year, with months as keys and counts as values
        grouped_data[year][month] = count
    
    # Convert defaultdict to regular dict for output
    return dict(grouped_data)




def retrieve_data_from_s3_df_for_employee_growth_per_quater_for_each_domain():

    df=InitialData().get_instance().get_data()

    selected_columns = df[['domain_name', 'employee_count_by_month']]

    selected_columns = selected_columns.dropna(subset=['domain_name', 'employee_count_by_month'])

    selected_columns = selected_columns[selected_columns['domain_name'].apply(lambda x: isinstance(x, str) and pd.notna(x))]

    selected_columns['employee_count_by_month'] = selected_columns['employee_count_by_month'].apply(convert_to_dict)

    selected_columns = selected_columns[selected_columns['employee_count_by_month'].notna()]

    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)  # Prevent wrapping the output to the next line
    pd.set_option('display.max_rows', None)  # Display all rows without truncation

    selected_columns['employee_count_by_month'] = selected_columns['employee_count_by_month'].apply(group_by_year)
    return selected_columns

def calculate_percent_increase_in_employee_count(yearly_grouped_employee_count_by_month):
    percent_increase_in_employee_count={}
    previous_quater_employee_count=None
    for year in yearly_grouped_employee_count_by_month.keys():
        one_year_data=yearly_grouped_employee_count_by_month[year]
        percent_increase_for_current_year,prev_quater_employee_count=calculate_percent_increase_in_employee_count_per_quater(one_year_data,previous_quater_employee_count,year)
        percent_increase_in_employee_count=percent_increase_in_employee_count|percent_increase_for_current_year
        previous_quater_employee_count=prev_quater_employee_count
    
    return percent_increase_in_employee_count
  

# Function to calculate the percentage increase in employee count per quarter per domain for one year
def calculate_percent_increase_in_employee_count_per_quater(one_year_data,prev_quater_employee_count,year):
    total_employee_count_for_current_quater=0
    percent_increase_for_current_year={}
    
    start_month=max(1, min(one_year_data.keys()))
    end_month=min(12,max(one_year_data.keys()))

    for month in range(start_month, end_month + 1):
        employee_count=0
        if(one_year_data.get(month) is not None):
            employee_count=one_year_data[month]
        if(isinstance(employee_count,int)):
            total_employee_count_for_current_quater+=employee_count
        if(month%3==0):
            if(prev_quater_employee_count is None or prev_quater_employee_count==0):
                percent_increase_for_current_year[get_quater_from_month(month,year)]=None
            else:
                percent_increase_for_current_year[get_quater_from_month(month,year)]=round(((total_employee_count_for_current_quater-prev_quater_employee_count)/prev_quater_employee_count)*100,2)
            prev_quater_employee_count=total_employee_count_for_current_quater
            total_employee_count_for_current_quater=0

#   handling the case when the year is not complete
    if(total_employee_count_for_current_quater>0):
        prev_quater_employee_count=total_employee_count_for_current_quater

    return percent_increase_for_current_year,prev_quater_employee_count

def get_quater_from_month(month,year):
    if(month>=1 and month<=3):
        return f"Q1 {year}"
    elif(month>=4 and month<=6):
        return f"Q2 {year}"
    elif(month>=7 and month<=9):
        return f"Q3 {year}"
    else:
        return f"Q4 {year}"


def processed_data():
    initial_data=retrieve_data_from_s3_df_for_employee_growth_per_quater_for_each_domain()
    final_data=[]
    for i in range(len(initial_data)):
        row=initial_data.iloc[i]
        domain_name=row['domain_name']
        grouped_employee_count_by_month=row['employee_count_by_month']  
        percent_increase_in_employee_count_per_quater_for_current_domain=calculate_percent_increase_in_employee_count(grouped_employee_count_by_month)   
        for quater in percent_increase_in_employee_count_per_quater_for_current_domain.keys():
            percent_increase=percent_increase_in_employee_count_per_quater_for_current_domain[quater]
            final_data.append({DOMAIN_NAME: domain_name,QUATER:quater,PERCENT_INCREASE:percent_increase,TENANT_ID:constants.TENANT_ID})
    return final_data


