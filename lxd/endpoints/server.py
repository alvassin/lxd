from typing import Any, Callable, Mapping

from lxd.endpoints.base import BaseApiEndpoint
from lxd.entities.server import Server, ServerResources


class ServerEndpoint(BaseApiEndpoint):
    URL_PATH = '/1.0'

    async def get(self, public: bool = False) -> Server:
        params = {}
        if public:
            params['public'] = True
        resp_content = await self._transport.get(self.URL_PATH, params=params)
        return Server.from_dict(resp_content.metadata)

    async def get_resources(self) -> ServerResources:
        resp_content = await self._transport.get(f'{self.URL_PATH}/resources')
        return ServerResources.from_dict(resp_content.metadata)

    async def partially_update_configuration(self, config: Mapping[str, Any]):
        await self._transport.patch(self.URL_PATH, json=config)

    async def update_configuration(self, config: Mapping[str, Any]):
        await self._transport.put(self.URL_PATH, json=config)

    async def register_event_handler(self, callback: Callable):
        async with self._transport.session.ws_connect('/1.0/events') as ws:
            async for msg in ws:
                await callback(msg)
