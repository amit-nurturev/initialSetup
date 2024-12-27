import sys
sys.path.append('../../..')

from domains.new_dev_project.core import db_insertion_facade
from utils.common_utils import get_request_id
import utils.logger as logger

def dump_employee_increase_per_quater_per_domain(event):
    req_id = get_request_id()
    logger.info(req_id, f"Inside dump_employee_increase_per_quater_per_domain with event")
    facade = db_insertion_facade.DbInserter(req_id)
    iam_response = facade.insert_employee_growth_per_quater_per_domain()
    return iam_response

def dump_employee_increase_per_role_per_quater_per_domain(event):
    req_id=get_request_id()
    logger.info(req_id, f"Inside dump_employee_increase_per_role_quater_per_domain with event")
    facade = db_insertion_facade.DbInserter(req_id)
    iam_response = facade.insert_employee_growth_per_role_per_quater_per_domain()
    return iam_response

def invoke_function_by_name(fn_name, fn_params):
    req_id = get_request_id()
    function = action_to_function_map.get(fn_name, None)
    if function is not None:
        try:
            response = function(req_id, fn_params)
            return {"statusCode": 200, "body": response}
        except Exception as err:
            logger.error(req_id, 500, f"Error in calling {fn_name} : " + err.args[0])
            traceback.print_exc()
            raise custom_excpt.MyError(
                error_code=500,
                error_message=f"unable to invoke {fn_name} err ${err.args[0]}",
                error_data=fn_params,
            )
    else:
        err = {
            "error_code": 404,
            "error_message": "Invoking unknown function : " + str(fn_name),
        }
        logger.error(req_id, err["error_code"], err["error_message"])
        return {"statusCode": 404, "body": err["error_message"]}


action_to_function_map={
    
}