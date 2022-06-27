from abc import ABC, abstractmethod

from mashumaro import DataClassDictMixin

from lxd.exceptions import LxdClientError


class BaseEntity(DataClassDictMixin):
    pass


class EntityLink(ABC):
    URL_PATH_PREFIX: str

    def __init__(self, endpoint):
        self._endpoint = endpoint

    @classmethod
    def parse_url_path(cls, url_path: str) -> str:
        if not url_path.startswith(cls.URL_PATH_PREFIX):
            raise LxdClientError(f'Unvalid url path {url_path}')
        return url_path[len(cls.URL_PATH_PREFIX):]

    @classmethod
    @abstractmethod
    def from_url_path(cls, endpoint, url_path: str):
        ...
