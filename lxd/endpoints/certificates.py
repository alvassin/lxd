import binascii
from typing import List, Union, Optional

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._serialization import Encoding

from lxd.endpoints.base import BaseApiEndpoint
from lxd.entities.certificates import Certificate, CertificateLink


class CertificatesEndpoint(BaseApiEndpoint):
    URL_PATH = '/1.0/certificates'

    async def list(
        self,
        recursion: int = 1
    ) -> Union[List[Certificate], List[CertificateLink]]:
        resp = await self._transport.get(
            self.URL_PATH, params={'recursion': recursion}
        )
        if recursion == 0:
            return [
                CertificateLink.from_url_path(self, url_path)
                for url_path in resp.metadata
            ]

        return [Certificate.from_dict(item) for item in resp.metadata]

    async def add(
        self,
        certificate: Union[str, bytes],
        type: str = 'client',
        name: Optional[str] = None,
        restricted: bool = False,
        projects: Optional[List[str]] = None,
        password: Optional[str] = None
    ):
        json = {'certificate': str(certificate), 'type': type}
        if name is not None:
            json['name'] = name
        if restricted:
            json['restricted'] = restricted
        if projects:
            json['projects'] = projects
        if password:
            json['password'] = password

        await self._transport.post(self.URL_PATH, json=json)

    async def get(self, fingerprint: str) -> Certificate:
        resp = await self._transport.get(f'{self.URL_PATH}/{fingerprint}')
        return Certificate.from_dict(resp.metadata)

    async def update_configuration_subset(
        self,
        fingerprint: str,
        certificate: Optional[Union[str, bytes]] = None,
        name: str = None,
        projects: str = None,
        restricted: bool = None,
        type: str = None
    ) -> None:
        json = {}
        if certificate is not None:
            json['certificate'] = certificate
        if name is not None:
            json['name'] = name
        if projects is not None:
            json['projects'] = projects
        if restricted is not None:
            json['restricted'] = restricted
        if type is not None:
            json['type'] = type

        await self._transport.patch(
            f'{self.URL_PATH}/{fingerprint}', json=json
        )

    async def update_configuration(
        self,
        fingerprint: str,
        certificate: Union[str, bytes],
        name: str,
        projects: str,
        restricted: bool,
        type: str
    ) -> None:
        json = {
            'certificate': str(certificate),
            'name': name,
            'projects': projects,
            'restricted': restricted,
            'type': type
        }
        await self._transport.put(f'{self.URL_PATH}/{fingerprint}', json=json)

    async def remove(self, fingerprint: str) -> None:
        await self._transport.get(f'{self.URL_PATH}/{fingerprint}')
