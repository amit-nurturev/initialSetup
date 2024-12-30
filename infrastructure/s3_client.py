import sys
sys.path.append("..")
import pandas as pd
from constants import constants
from utils.exception import *

    
def read_file_from_s3_into_df(bucket_name,filepath,file_format,index_col=0):
    s3_path=f"s3://{bucket_name}/{filepath}"
    if(file_format==constants.FILE_FORMAT_CSV):
        print(f"downloading {file_format} from {s3_path})")
        df=pd.read_csv(s3_path,index_col=index_col)
        return df
    else:
        raise MyError(error_code=400,error_message="Cannot process data, input file type not supported yet!")
        
