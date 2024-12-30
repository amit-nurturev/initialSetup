import sys
sys.path.append('.')
import json
from domains.new_dev_project.application.data_insertion_controller import invoke_function_by_name
from constants.constants import USER_ID_FIELD,TENANT_ID_FIELD
from utils.exception import MyError

route_to_function_map= {
    "/dump/inc_per_quater_per_domain":"dump_employee_increase_per_quater_per_domain",

    "/dump/inc_per_quater_per_role_per_domain":"dump_employee_increase_per_role_per_quater_per_domain"
}

def get_user_and_tenant(event: dict):
    requestContext: dict = event.get("requestContext", {})
    authorizer: dict = requestContext.get("authorizer", {})
    lamb_da: dict = authorizer.get("lambda", {})
    user_id = lamb_da.get("user_id", None)
    tenant_id = lamb_da.get("tenant_id", 202)
    return user_id, tenant_id


def get_api_gateway_function_params(event: dict):
    headers = event["headers"]
    method = event["requestContext"]["http"]["method"]
    route = event["routeKey"].split(" ")[1]
    fn_name = route_to_function_map.get(route, "")
    fn_params = dict()
    if method == "GET":
        fn_params = event["pathParameters"]
    else:
        try:
            fn_params = json.loads(event["body"])
        except KeyError:
            fn_params = dict()
    user_id, tenant_id = get_user_and_tenant(event)
    fn_params[USER_ID_FIELD] = user_id
    if TENANT_ID_FIELD not in fn_params:
        fn_params[TENANT_ID_FIELD] = tenant_id
    print("fn_name", fn_name)
    print("fn_params", fn_params)
    return fn_name, fn_params


def handler(event, context):
    print(" event in db_dump_lambda_handler ", event)
    print(" context in db_dump_lambda_handler ",context)
    # when lambda is invoked from api gateway, it adds rawPath param in the event.
    if "rawPath" in event:
        fn_name, fn_params = get_api_gateway_function_params(event)
    else:
        fn_name, fn_params = get_default_params(event)
    if(fn_name is None):
        raise MyError(404,'No function name found.')
    
    return invoke_function_by_name(fn_name, fn_params)


def get_default_params(event):
    error = event.get("Error", None)
    if error:
       print('even has error and hence denying the function calling')
       return None, None
    
    body: dict = event.get('body',{})
    fn_params = {
        USER_ID_FIELD: body.get(USER_ID_FIELD, ""),
        TENANT_ID_FIELD: body.get(TENANT_ID_FIELD, ""),
    }
    fn_name = route_to_function_map["/dump/inc_per_quater_per_domain"]
    return fn_name, fn_params



if __name__ == "__main__":
    event = {}
    handler(event, None)