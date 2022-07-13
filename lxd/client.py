from pathlib import Path

from lxd.endpoints.certificates import CertificatesEndpoint
from lxd.endpoints.instances import InstancesEndpoint
from lxd.endpoints.operations import OperationsEndpoint
from lxd.endpoints.server import ServerEndpoint
from lxd.transport import LXDTransport


class LXDClient:
    def __init__(self, transport: LXDTransport):
        self.transport = transport

        self.operations = OperationsEndpoint(self.transport)
        self.instances = InstancesEndpoint(self.transport)
        self.certificates = CertificatesEndpoint(self.transport)
        self.server = ServerEndpoint(self.transport)

    async def authenticate(self, cert_path: Path, password: str):
        server_info = await self.server.get()
        if server_info.auth == 'trusted':
            return

        with open(cert_path.expanduser(), 'rb') as f:
            cert = f.read()
        await self.certificates.add(cert, password=password)
