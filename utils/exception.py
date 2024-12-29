class MyError(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(f"Error code {error_code}: {error_message}")

    def __getitem__(self, key):
        if key == 'error_code':
            return self.error_code
        elif key == 'error_message':
            return self.error_message
        else:
            raise KeyError(f"{key} not found in MyError")
        