from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Mapping, Optional, Union, Dict

from lxd.entities.base import BaseEntity
from lxd.entities.operations import Operation
from lxd.utils import parse_datetime_with_nanoseconds


@dataclass(frozen=True)
class Server(BaseEntity):
    api_extensions: List[str]
    api_status: str
    api_version: str
    auth: str
    auth_methods: List[str]
    public: bool
    config: Optional[Mapping[str, Any]] = None
    environment: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class ServerResources(BaseEntity):
    cpu: Mapping[str, Any]
    memory: Mapping[str, Any]
    gpu: Mapping[str, Any]
    network: Mapping[str, Any]
    storage: Mapping[str, Any]
    usb: Mapping[str, Any]
    pci: Mapping[str, Any]
    system: Mapping[str, Any]


@dataclass(frozen=True)
class LoggingEvent(BaseEntity):
    message: str
    level: str
    context: Mapping[str, Any]


@dataclass(frozen=True)
class LifecycleEvent(BaseEntity):
    action: str
    source: str
    requestor: Mapping[str, Any]
    context: Optional[Mapping[str, Any]] = None


@dataclass(frozen=False)
class Event(BaseEntity):
    location: str
    metadata: Union[LifecycleEvent, LoggingEvent, Operation]
    timestamp: datetime = field(metadata={
        "deserialize": parse_datetime_with_nanoseconds
    })
    type: str
    project: Optional[str] = None
