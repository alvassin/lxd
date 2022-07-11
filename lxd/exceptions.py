class LxdClientError(RuntimeError):
    def __init__(self, error: str):
        self.error = error
