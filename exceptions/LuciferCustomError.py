class LuciferCustomError(Exception):
    def __init__(self, message="An error occurred", code=None):
        super().__init__(message)
        self.code = code
        self.message = message
