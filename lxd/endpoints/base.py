from lxd.transport import Transport


class BaseApiEndpoint:
    URL_PATH: str

    def __init__(self, transport: Transport):
        self._transport = transport
