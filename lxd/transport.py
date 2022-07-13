import os
from pathlib import Path
from ssl import SSLContext
from typing import Optional

from aiohttp import (
    BaseConnector, ClientResponseError, ClientSession, TCPConnector,
    UnixConnector, hdrs
)
from aiohttp.typedefs import StrOrURL
from yarl import URL

from lxd.entities.response import Response


class LXDTransport:
    def __init__(
        self, *,
        endpoint_url: Optional[StrOrURL] = None,
        cert_path: Optional[Path] = None,
        key_path: Optional[Path] = None,
        endpoint_cert_path: Optional[Path] = None,
        session: Optional[ClientSession] = None,
        connector: Optional[BaseConnector] = None,
    ):
        """Constructs transport for LXD client.
        :param endpoint_url: endpoint can be an http endpoint or a path to a
            unix socket.
        :param cert_path: Path to client certificate to use for client
            authentication.
        :param key_path: Path to private key to use with client certificate for
            client authentication.
        :param session: Preconfigured aiohttp ClientSession object.
        :param connector: Preconfigured aiohttp BaseConnector descendant
            object.
        """
        if session is not None and any((
            endpoint_url, cert_path, key_path, endpoint_cert_path, connector
        )):
            raise ValueError(
                'session parameter does not allow passing other parameters'
            )

        if connector is not None and any((
            cert_path, key_path, endpoint_cert_path
        )):
            raise ValueError(
                'connector parameter does not allow passing cert_path, '
                'key_path, endpoint_cert_path parameters'
            )

        self._session_owner = False

        if session:
            self._session = session
            return

        connector_owner = False
        if connector is None:
            connector_owner = True
            if endpoint_url is None:
                path = '/var/lib/lxd/unix.socket'
                if 'LXD_DIR' in os.environ:
                    path = str(Path(os.environ.get('LXD_DIR')) / 'unix.socket')
                elif Path('/var/snap/lxd/common/lxd/unix.socket').is_socket():
                    path = '/var/snap/lxd/common/lxd/unix.socket'
                endpoint_url = URL.build(scheme='unix', path=path)

            endpoint_url = URL(endpoint_url)
            if endpoint_url.scheme == 'unix':
                connector = UnixConnector(endpoint_url.path)
                endpoint_url = URL.build(
                    scheme='http', host='lxd', path=endpoint_url.path
                )
            elif endpoint_url.scheme == 'https':
                ssl_ctx = SSLContext()
                if endpoint_cert_path:
                    ssl_ctx.load_verify_locations(
                        endpoint_cert_path.expanduser()
                    )
                ssl_ctx.load_cert_chain(
                    str(cert_path.expanduser()), str(key_path.expanduser())
                )
                connector = TCPConnector(ssl_context=ssl_ctx)
            else:
                raise ValueError(f'Unsupported scheme {endpoint_url.scheme}')

        self._session = ClientSession(
            base_url=endpoint_url,
            connector=connector,
            connector_owner=connector_owner,
            raise_for_status=True,
        )
        self._session_owner = True

    async def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    async def close(self):
        if not self._session_owner:
            return
        await self._session.close()

    @property
    def session(self) -> ClientSession:
        return self._session

    async def request(self, method: str, url: StrOrURL, **kwargs) -> Response:
        async with self._session.request(
            method, url, **kwargs, raise_for_status=False
        ) as resp:
            body = await resp.json()
            if resp.ok:
                return Response.from_dict(body)

            raise ClientResponseError(
                resp.request_info,
                resp.history,
                status=resp.status,
                message=body.get('error', resp.reason),
                headers=resp.headers,
            )

    def head(self, url: StrOrURL, **kwargs):
        return self.request(hdrs.METH_HEAD, url, **kwargs)

    def get(self, url: StrOrURL, **kwargs):
        return self.request(hdrs.METH_GET, url, **kwargs)

    def post(self, url: StrOrURL, **kwargs):
        return self.request(hdrs.METH_POST, url, **kwargs)

    def patch(self, url: StrOrURL, **kwargs):
        return self.request(hdrs.METH_PATCH, url, **kwargs)

    def put(self, url: StrOrURL, **kwargs):
        return self.request(hdrs.METH_PUT, url, **kwargs)

    def delete(self, url: StrOrURL, **kwargs):
        return self.request(hdrs.METH_DELETE, url, **kwargs)
