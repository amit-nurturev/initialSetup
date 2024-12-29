import sys
import json
import boto3

sys.path.append('.')


class Lambda:
    """ AWS Lambda client, all Lambda client functions go here
    """
    client = None

    def __init__(self) -> None:
        self.client = boto3.client('lambda')

    def invoke_function(self, fn_name: str, payload: dict):
        """_summary_

        Args:
            fn_name (str): lambda function name
            payload (dict): lambda payload

        Returns:
            _type_: lambda response
        """
        response = self.client.invoke(
            FunctionName=fn_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        return response