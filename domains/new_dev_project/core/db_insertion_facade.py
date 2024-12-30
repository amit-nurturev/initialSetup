import sys
sys.path.append("../../..")

from utils.exception import MyError
from domains.new_dev_project.core.port.incoming import processed_data_interface
from infrastructure.postgres_connector import DB_Client
from utils.data_preprocessing import employee_growth_per_quater_per_domain, employee_growth_per_role_per_quater_per_domain
from constants.constants import EMPLOYEE_GROWTH_PER_QUATER,EMPLOYEE_GROWTH_PER_ROLE_PER_QUATER

class DbInserter(processed_data_interface.ProcessedDataInterface):
    req_id=None
    
    def __init__(self,req_id):
        self.req_id=req_id
    
    def processed_data_for_employee_growth_per_quater_per_domain(self):
        return employee_growth_per_quater_per_domain.processed_data()
    
    def processed_data_for_employee_growth_per_role_per_quater_per_domain(self):
        return employee_growth_per_role_per_quater_per_domain.processed_data()
    
    def insert_employee_growth_per_quater_per_domain(self):
        try:
            processed_data = self.processed_data_for_employee_growth_per_quater_per_domain()
            with DB_Client() as db_client:
                return db_client.insert_row_into_table(EMPLOYEE_GROWTH_PER_QUATER, processed_data)
        except Exception as e:
                raise MyError(400,f"Failed to insert data into {EMPLOYEE_GROWTH_PER_QUATER}: {e}")


    def insert_employee_growth_per_role_per_quater_per_domain(self):
        try:
            processed_data = self.processed_data_for_employee_growth_per_role_per_quater_per_domain()
            with DB_Client() as db_client:
                return db_client.insert_row_into_table(EMPLOYEE_GROWTH_PER_ROLE_PER_QUATER, processed_data)
        except Exception as e:
                raise MyError(400,f"Failed to insert data into {EMPLOYEE_GROWTH_PER_ROLE_PER_QUATER}: {e}")
