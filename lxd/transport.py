from http import HTTPStatus
from typing import Mapping

from aiohttp import ClientSession, hdrs
from aiohttp.typedefs import StrOrURL

from lxd.entities.response import Response
from lxd.exceptions import LxdApiForbidden, LxdApiNotFound


class Transport:
    def __init__(self, session: ClientSession):
        self._session = session

    @property
    def session(self) -> ClientSession:
        return self._session

    async def request(self, method: str, url: StrOrURL, **kwargs):
        async with self._session.request(
            method, url, **kwargs, raise_for_status=False
        ) as resp:
            raw_content = await resp.json()
            return self._handle_response(resp.status, raw_content)

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

    @staticmethod
    def _handle_response(status: int, raw_content: Mapping):
        content = Response.from_dict(raw_content)
        if status == HTTPStatus.FORBIDDEN:
            raise LxdApiForbidden(content.error_code, content.error)
        elif status == HTTPStatus.NOT_FOUND:
            raise LxdApiNotFound(content.error_code, content.error)
        return content
