import binascii
from typing import List, Union

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
        cert_data: bytes,
        password: str,
        type: str = 'client'
    ) -> CertificateLink:
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        base64_cert = cert.public_bytes(Encoding.PEM).decode('utf-8')
        base64_cert = '\n'.join(base64_cert.split('\n')[1:-2])

        data = {'certificate': base64_cert, 'type': type, 'password': password}
        await self._transport.post(self.URL_PATH, json=data)
        fingerprint = binascii.hexlify(
            cert.fingerprint(hashes.SHA256())).decode(
            'utf-8'
        )
        return CertificateLink(endpoint=self, fingerprint=fingerprint)

    async def get(self, fingerprint: str) -> Certificate:
        resp = await self._transport.get(f'{self.URL_PATH}/{fingerprint}')
        return Certificate.from_dict(resp.metadata)

    async def partial_update(
        self,
        fingerprint: str,
        certificate: str = None,
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

    async def update(
        self,
        fingerprint: str,
        certificate: str,
        name: str,
        projects: str,
        restricted: bool,
        type: str
    ) -> None:
        await self._transport.put(
            f'{self.URL_PATH}/{fingerprint}',
            json={
                'certificate': certificate,
                'name': name,
                'projects': projects,
                'restricted': restricted,
                'type': type
            }
        )

    async def delete(self, fingerprint: str) -> None:
        await self._transport.get(f'{self.URL_PATH}/{fingerprint}')
