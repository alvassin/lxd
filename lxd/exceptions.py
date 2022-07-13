class LXDClientError(RuntimeError):
    def __init__(self, error: str):
        self.error = error
