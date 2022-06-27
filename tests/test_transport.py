import pytest

from lxd.exceptions import LxdApiForbidden, LxdApiNotFound
from lxd.transport import Transport


@pytest.mark.parametrize('resp_code,resp_content,expected_exc', (
    (
        403,
        {
            'type': 'error',
            'error': 'not authorized',
            'error_code': 403,
            'status': '',
            'status_code': 0,
            'operation': '',
            'metadata': None
        },
        LxdApiForbidden
    ),
    (
        404,
        {
            'type': 'error',
            'status': '',
            'status_code': 0,
            'operation': '',
            'error_code': 404,
            'error': 'not found',
            'metadata': None
        },
        LxdApiNotFound
    )
))
def test_handle_error_response(resp_code, resp_content, expected_exc):
    with pytest.raises(expected_exc) as exc:
        Transport._handle_response(resp_code, resp_content)

    assert exc.value.error_code == resp_code
    assert exc.value.error == resp_content['error']
