from pathlib import Path
from ssl import SSLContext
from typing import Optional

from aiohttp import ClientSession, TCPConnector
from aiohttp.typedefs import StrOrURL

from lxd.endpoints.certificates import CertificatesEndpoint
from lxd.endpoints.instances import InstancesEndpoint
from lxd.endpoints.operations import OperationsEndpoint
from lxd.endpoints.server import ServerEndpoint
from lxd.transport import Transport


class LXDClient:
    def __init__(self, session: ClientSession):
        self.transport = Transport(session)

        self.operations = OperationsEndpoint(self.transport)
        self.instances = InstancesEndpoint(self.transport)
        self.certificates = CertificatesEndpoint(self.transport)
        self.server = ServerEndpoint(self.transport)

    async def authenticate(self, cert_path: Path, password: str):
        server_info = await self.server.get()
        if server_info.auth == 'trusted':
            return

        with open(cert_path.expanduser()) as f:
            cert = f.read().encode('utf-8')

        await self.certificates.add(cert, password=password)


def lxd_client(
    endpoint_url: StrOrURL,
    cert_path: Path,
    key_path: Path,
    endpoint_cert_path: Optional[Path] = None
) -> LXDClient:
    ssl_ctx = SSLContext()
    if endpoint_cert_path:
        ssl_ctx.load_verify_locations(endpoint_cert_path.expanduser())
    ssl_ctx.load_cert_chain(
        str(cert_path.expanduser()), str(key_path.expanduser())
    )

    connector = TCPConnector(ssl_context=ssl_ctx)
    session = ClientSession(
        base_url=endpoint_url, connector=connector, raise_for_status=True
    )
    return LXDClient(session=session)
