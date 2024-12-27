"""Step function handler"""
import sys
sys.path.append('.')
import json
import boto3


class StepFunction:
    """ AWS Step function client
    """
    client = None

    def __init__(self) -> None:
        self.client = boto3.client('stepfunctions')

    def start_execution(self, fn_arn: str, payload: dict):
        """_summary_

        Args:
            fn_arn (str): step function arn
            payload (dict): function input

        Returns:
            step function response
        """
        response = self.client.start_execution(
            stateMachineArn=fn_arn,
            input=json.dumps(payload)
        )
        return response