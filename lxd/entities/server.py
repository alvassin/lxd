from dataclasses import dataclass
from typing import Any, List, Mapping, Optional

from lxd.entities.base import BaseEntity


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
