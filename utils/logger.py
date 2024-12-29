def info(req_id, message):
    info_message = f"req_id: {req_id} , Log : {message}"
    print(info_message)

def error(req_id, error_code, message):
    error_message = f"req_id: {req_id} , error_code : {error_code}, Error : {message}"
    print(error_message)