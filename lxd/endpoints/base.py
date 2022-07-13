from lxd.transport import LXDTransport


class BaseApiEndpoint:
    URL_PATH: str

    def __init__(self, transport: LXDTransport):
        self._transport = transport
