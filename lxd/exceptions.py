class LxdClientError(RuntimeError):
    def __init__(self, error: str):
        self.error = error


class LxdApiError(RuntimeError):
    def __init__(self, error_code: int, error: str = None):
        self.error_code = error_code
        self.error = error


class LxdApiForbidden(LxdApiError):
    pass


class LxdApiNotFound(LxdApiError):
    pass
