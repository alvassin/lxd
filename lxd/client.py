from contextlib import asynccontextmanager
from pathlib import Path
from ssl import SSLContext
from typing import AsyncContextManager, Optional

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

        with open(cert_path.expanduser(), 'rb') as f:
            cert = f.read()
        await self.certificates.add(cert, password=password)


@asynccontextmanager
async def make_client(
    endpoint_url: StrOrURL,
    cert_path: Path,
    key_path: Path,
    endpoint_cert_path: Optional[Path] = None
) -> AsyncContextManager[LXDClient]:
    ssl_ctx = SSLContext()
    if endpoint_cert_path:
        ssl_ctx.load_verify_locations(endpoint_cert_path.expanduser())
    ssl_ctx.load_cert_chain(
        str(cert_path.expanduser()), str(key_path.expanduser())
    )

    async with ClientSession(
        base_url=endpoint_url,
        connector=TCPConnector(ssl_context=ssl_ctx),
        raise_for_status=True
    ) as session:
        yield LXDClient(session=session)
