from dataclasses import dataclass
from typing import List

from lxd.entities.base import BaseEntity, EntityLink


@dataclass(frozen=True)
class Certificate(BaseEntity):
    certificate: str
    fingerprint: str
    name: str
    projects: List[str]
    restricted: bool
    type: str


class CertificateLink(EntityLink):
    URL_PATH_PREFIX = '/1.0/certificates/'

    def __init__(self, endpoint, fingerprint: str):
        super().__init__(endpoint)
        self.fingerprint = fingerprint

    @classmethod
    def from_url_path(cls, endpoint, url_path: str) -> 'CertificateLink':
        return cls(endpoint=endpoint, fingerprint=cls.parse_url_path(url_path))

    def __await__(self) -> Certificate:
        return self._endpoint.get(self.fingerprint).__await__()
