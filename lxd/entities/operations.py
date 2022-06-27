from dataclasses import dataclass, field
from typing import Mapping

from mashumaro import field_options

from lxd.entities.base import BaseEntity, EntityLink


@dataclass(frozen=True)
class Operation(BaseEntity):
    class_: str = field(metadata=field_options(alias='class'))
    description: str
    err: str
    id: str
    location: str
    may_cancel: bool
    metadata: Mapping
    resources: Mapping
    status: str
    status_code: int
    created_at: str
    updated_at: str


class OperationLink(EntityLink):
    URL_PATH_PREFIX = '/1.0/operations/'

    def __init__(self, endpoint, id: str):
        super().__init__(endpoint)
        self.id = id

    @classmethod
    def from_url_path(cls, endpoint, url_path: str) -> 'OperationLink':
        return cls(endpoint=endpoint, id=cls.parse_url_path(url_path))

    def __await__(self) -> Operation:
        return self._endpoint.get(self.id).__await__()
