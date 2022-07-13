import itertools
import os
from unittest import mock

import pytest
from aiohttp import ClientSession, TCPConnector, UnixConnector

from lxd import LXDTransport


def test_create_unix_socket_transport():
    transport = LXDTransport()
    assert isinstance(transport.session.connector, UnixConnector)
    assert transport.session._base_url.scheme == 'http'
    assert transport.session._base_url.host == 'lxd'
    assert transport.session._base_url.path == '/var/lib/lxd/unix.socket'


def test_create_unix_socket_transport_with_specific_path():
    transport = LXDTransport(endpoint_url='unix:///custom/lxd/socket.path')
    assert isinstance(transport.session.connector, UnixConnector)
    assert transport.session._base_url.scheme == 'http'
    assert transport.session._base_url.host == 'lxd'
    assert transport.session._base_url.path == '/custom/lxd/socket.path'


def test_create_unix_socket_transport_with_env_var():
    with mock.patch.dict(os.environ, {'LXD_DIR': '/custom/lxd'}):
        transport = LXDTransport()
        assert isinstance(transport.session.connector, UnixConnector)
        assert transport.session._base_url.scheme == 'http'
        assert transport.session._base_url.host == 'lxd'
        assert transport.session._base_url.path == '/custom/lxd/unix.socket'


def test_create_https_transport(assets_path):
    transport = LXDTransport(
        endpoint_url='https://127.0.0.1:8443',
        cert_path=assets_path / 'certificate.pem',
        key_path=assets_path / 'private-key.pem'
    )
    assert isinstance(transport.session.connector, TCPConnector)
    assert transport.session._base_url.scheme == 'https'
    assert transport.session._base_url.host == '127.0.0.1'
    assert transport.session._base_url.port == 8443
    assert transport.session._base_url.path == '/'


def test_create_https_transport_with_endpoint_cert(assets_path):
    transport = LXDTransport(
        endpoint_url='https://127.0.0.1:8443',
        cert_path=assets_path / 'certificate.pem',
        key_path=assets_path / 'private-key.pem',
        endpoint_cert_path=assets_path / 'certificate.pem'
    )
    assert isinstance(transport.session.connector, TCPConnector)
    assert transport.session._base_url.scheme == 'https'
    assert transport.session._base_url.host == '127.0.0.1'
    assert transport.session._base_url.port == 8443
    assert transport.session._base_url.path == '/'


async def test_create_transport_with_session():
    session = ClientSession()
    transport = LXDTransport(session=session)
    await transport.close()
    assert session.closed is False, 'transport closed not owned session'


async def test_create_transport_with_connector():
    connector = TCPConnector()
    transport = LXDTransport(connector=connector)
    await transport.close()
    assert connector.closed is False, 'transport closed not owned connector'


def test_create_transport_with_session_invalid_params(assets_path):
    not_allowed_params = {
        'endpoint_url': 'https://127.0.0.1',
        'cert_path': assets_path / 'certificate.pem',
        'key_path': assets_path / 'private-key.pem',
        'endpoint_cert_path': assets_path / 'certificate.pem',
        'connector': TCPConnector()
    }

    for params_number in range(1, len(not_allowed_params) + 1):
        for param_names in itertools.combinations(
            not_allowed_params.keys(), params_number
        ):
            kwargs = {
                param: not_allowed_params[param] for param in param_names
            }
            with pytest.raises(ValueError) as e:
                LXDTransport(session=ClientSession(), **kwargs)

            assert str(e.value) == (
                'session parameter does not allow passing other parameters'
            )


def test_create_transport_with_connector_invalid_params(assets_path):
    not_allowed_params = {
        'cert_path': assets_path / 'certificate.pem',
        'key_path': assets_path / 'private-key.pem',
        'endpoint_cert_path': assets_path / 'certificate.pem',
    }

    for params_number in range(1, len(not_allowed_params) + 1):
        for param_names in itertools.combinations(
            not_allowed_params.keys(), params_number
        ):
            kwargs = {
                param: not_allowed_params[param] for param in param_names
            }
            with pytest.raises(ValueError) as e:
                LXDTransport(connector=TCPConnector(), **kwargs)

            assert str(e.value) == (
                'connector parameter does not allow passing cert_path, '
                'key_path, endpoint_cert_path parameters'
            )
