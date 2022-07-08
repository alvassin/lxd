from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Mapping, Optional

from lxd.entities.base import BaseEntity, EntityLink
from lxd.utils import parse_datetime_with_nanoseconds


@dataclass(frozen=True)
class InstanceBackup(BaseEntity):
    name: str
    container_only: bool
    instance_only: bool
    optimized_storage: bool
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True)
class InstanceSnapshot(BaseEntity):
    architecture: str
    config: Mapping
    created_at: datetime
    last_used_at: datetime
    expires_at: datetime
    devices: Mapping
    ephemeral: bool
    expanded_config: Mapping
    expanded_devices: Mapping
    name: str
    profiles: List[str]
    size: int
    stateful: bool


@dataclass(frozen=True)
class InstanceState(BaseEntity):
    status: str
    status_code: int
    disk: Mapping
    memory: Mapping
    network: Mapping
    pid: int
    processes: int
    cpu: Mapping


@dataclass(frozen=True)
class BaseInstance(BaseEntity):
    architecture: str
    config: Mapping
    devices: Mapping
    name: str
    type: str
    description: str
    stateful: str
    ephemeral: bool


@dataclass(frozen=True)
class Instance(BaseInstance):
    status: str
    status_code: int
    project: str
    profiles: List[str]
    expanded_config: Mapping[str, Any]
    expanded_devices: Mapping[str, Any]
    location: str
    created_at: datetime = field(metadata={
        'deserialize': parse_datetime_with_nanoseconds
    })
    last_used_at: datetime = field(metadata={
        'deserialize': parse_datetime_with_nanoseconds
    })
    backups: Optional[List[InstanceBackup]] = None
    snapshots: Optional[List[InstanceSnapshot]] = None
    state: Optional[InstanceState] = None


@dataclass(frozen=True)
class InstanceCreateRequest(BaseInstance):
    instance_type: str
    restore: str
    source: str


class InstanceLink(EntityLink):
    URL_PATH_PREFIX = '/1.0/instances/'

    def __init__(self, endpoint, name: str):
        super().__init__(endpoint)
        self.name = name

    @classmethod
    def from_url_path(cls, endpoint, url_path: str) -> 'InstanceLink':
        return cls(endpoint=endpoint, name=cls.parse_url_path(url_path))

    def __await__(self) -> Instance:
        return self._endpoint.get(self.name).__await__()


class InstanceAction(str, Enum):
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'
    FREEZE = 'freeze'
    UNFREEZE = 'unfreeze'
