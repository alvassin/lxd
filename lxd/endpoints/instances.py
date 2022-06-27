from typing import List, Optional, Union

from lxd.endpoints.base import BaseApiEndpoint
from lxd.entities.instances import (
    Instance, InstanceAction, InstanceCreateRequest, InstanceLink,
    InstanceState
)
from lxd.entities.operations import Operation


class InstancesEndpoint(BaseApiEndpoint):
    URL_PATH = '/1.0/instances'

    async def list(
        self,
        recursion: int = 1
    ) -> Union[List[Instance], List[InstanceLink]]:
        resp = await self._transport.get(
            self.URL_PATH, params={'recursion': recursion}
        )
        if recursion == 0:
            return [
                InstanceLink.from_url_path(self, url_path)
                for url_path in resp.metadata
            ]
        return [Instance.from_dict(item) for item in resp.metadata]

    async def get(self, name: str) -> Instance:
        resp = await self._transport.get(f'{self.URL_PATH}/{name}')
        return Instance.from_dict(resp.metadata)

    async def get_state(
        self,
        name: str,
        *,
        project: Optional[str] = None
    ) -> InstanceState:
        params = {'project': project} if project is not None else {}
        resp = await self._transport.get(
            f'{self.URL_PATH}/{name}/state', params=params
        )
        return InstanceState.from_dict(resp.metadata)

    async def update_state(
        self,
        name: str,
        *,
        action: InstanceAction,
        force: bool = False,
        stateful: bool = False,
        timeout: int = 30,
        project: str = None
    ) -> Operation:
        params = {'project': project} if project is not None else {}
        json = {
            'action': action.value,
            'force': force,
            'stateful': stateful,
            'timeout': timeout
        }

        resp = await self._transport.put(
            f'{self.URL_PATH}/{name}/state', params=params, json=json
        )
        return Operation.from_dict(resp.metadata)

    async def delete(self, name: str, project: str = None) -> Operation:
        params = {'project': project} if project is not None else {}
        resp = await self._transport.delete(
            f'{self.URL_PATH}/{name}', params=params
        )
        return Operation.from_dict(resp.metadata)

    async def create(
        self,
        instance: InstanceCreateRequest,
        project: str = None,
        target: str = None
    ) -> Operation:
        params = {}
        if project is not None:
            params['project'] = project
        if target is not None:
            params['target'] = target

        resp = await self._transport.put(
            self.URL_PATH, params=params, json=instance.to_dict()
        )
        return Operation.from_dict(resp.metadata)
