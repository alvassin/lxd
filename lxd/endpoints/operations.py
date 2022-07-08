from typing import List, Union

from lxd.endpoints.base import BaseApiEndpoint
from lxd.entities.operations import Operation, OperationLink


class OperationsEndpoint(BaseApiEndpoint):
    URL_PATH = '/1.0/operations'

    async def list(
        self,
        recursion: int = 0
    ) -> Union[List[Operation], List[OperationLink]]:
        resp = await self._transport.get(
            self.URL_PATH, params={'recursion': recursion}
        )
        if recursion == 0:
            return [
                OperationLink.from_url_path(self, url_path)
                for url_path in resp.metadata
            ]
        return [Operation.from_dict(item) for item in resp.metadata]

    async def get(self, operation_id: str) -> Operation:
        resp = await self._transport.get(f'{self.URL_PATH}/{operation_id}')
        return Operation.from_dict(resp.metadata)

    async def cancel(self, operation_id: str):
        await self._transport.delete(f'{self.URL_PATH}/{operation_id}')

    async def wait(
        self,
        operation_id: str,
        *,
        timeout: int = -1
    ) -> Operation:
        resp = await self._transport.get(
            f'{self.URL_PATH}/{operation_id}/wait',
            params={'timeout': timeout}
        )
        return Operation.from_dict(resp.metadata)
