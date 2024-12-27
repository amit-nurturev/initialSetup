import sys

sys.path.append(".")
sys.path.append("../..")
sys.path.append("../")
import os
from supabase import create_client, Client
import pandas as pd
from dotenv import load_dotenv
from constants.schema.emp_growth_per_quater_per_domain_fields import TENANT_ID, DOMAIN_NAME, QUATER, PERCENT_INCREASE

load_dotenv()


class DB_Client:
    supabase: Client = None

    def __enter__(self):
        self.initiate_supabase_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.supabase.postgrest.aclose()

    def initiate_supabase_client(self):
        print("url is",os.environ.get("SUPABASE_URL"))
        print("key is",os.environ.get("SUPABASE_KEY"))
        try:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
            supabase: Client = create_client(url, key)
            self.supabase = supabase
        except Exception as e:
            raise e
        else:
            print('initialize success')

    def insert_row_into_table(self, table_name, data):
        query = self.supabase.table(table_name).insert(json=data)
        response = query.execute().data
        df = pd.DataFrame(response)
        return df


data_entries = [
    {
        DOMAIN_NAME: "finance",
        QUATER: "2010 Q1",
        PERCENT_INCREASE: 12.5,
        TENANT_ID: 202
    }
]

if __name__ == "__main__":
    with DB_Client() as db_client:
        print(db_client.insert_row_into_table("employee_growth_per_quater", data_entries))
        