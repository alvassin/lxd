from typing import Any, Mapping, Optional

from aiohttp import WSMessage

from lxd.endpoints.base import BaseApiEndpoint
from lxd.entities.server import Event, Server, ServerResources


class ServerEndpoint(BaseApiEndpoint):
    URL_PATH = '/1.0'

    async def get(
        self,
        target: Optional[str] = None,
        project: Optional[str] = None
    ) -> Server:
        params = {}
        if target is not None:
            params['target'] = target
        if project is not None:
            params['project'] = project

        resp_content = await self._transport.get(self.URL_PATH, params=params)
        return Server.from_dict(resp_content.metadata)

    async def get_resources(self) -> ServerResources:
        resp_content = await self._transport.get(f'{self.URL_PATH}/resources')
        return ServerResources.from_dict(resp_content.metadata)

    async def update_configuration_subset(self, config: Mapping[str, Any]):
        await self._transport.patch(self.URL_PATH, json={'config': config})

    async def update_configuration(self, config: Mapping[str, Any]):
        await self._transport.put(self.URL_PATH, json={'config': config})

    async def get_events(
        self,
        project: Optional[str] = None,
        type: Optional[str] = None
    ):
        params = {}
        if project is not None:
            params['project'] = project
        if type is not None:
            params['type'] = type

        async with self._transport.session.ws_connect(
            f'{self.URL_PATH}/events', params=params
        ) as ws:
            msg: WSMessage
            async for msg in ws:
                yield Event.from_dict(msg.json())
