from aiohttp import ClientResponseError, ClientSession, hdrs
from aiohttp.typedefs import StrOrURL

from lxd.entities.response import Response


class Transport:
    def __init__(self, session: ClientSession):
        self._session = session

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
