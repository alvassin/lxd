from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from lxd.entities.base import BaseEntity


class OperationType(str, Enum):
    SYNC = 'sync'
    ASYNC = 'async'
    ERROR = 'error'


@dataclass(frozen=True)
class Response(BaseEntity):
    type: OperationType
    error: str
    error_code: int
    status: str
    status_code: int
    metadata: Any
    operation: Optional[str] = None
