import sys
sys.path.append('../../..')
from domains.new_dev_project.core.port.outgoing.initial_data import InitialDataInterface
from infrastructure.s3_client import read_file_from_s3_into_df
from constants import constants

class InitialData(InitialDataInterface):
    _cached_df=None
    _instance=None
    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if InitialData._instance is None:
            InitialData._instance = InitialData()
        return InitialData._instance

    def get_data(self):
        if self._cached_df is None:
            self._cached_df = read_file_from_s3_into_df(constants.BUCKET_NAME, constants.FILE_KEY, constants.FILE_FORMAT_CSV)
        return self._cached_df
