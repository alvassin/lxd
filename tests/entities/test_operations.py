from datetime import datetime, timezone

from lxd.entities.operations import Operation


def test_create_operation():
    operation = Operation.from_dict({
        'id': '195fdb8d-b74b-4baa-a977-c1da8a7570ad',
        'class': 'task',
        'description': 'Stopping instance',
        'created_at': '2022-07-01T20:09:18.699628368Z',
        'updated_at': '2022-07-01T20:09:18.699628368Z',
        'status': 'Running',
        'status_code': 103,
        'resources': {
            'instances': ['/1.0/instances/capital-redfish']
        },
        'metadata': None,
        'may_cancel': False,
        'err': '',
        'location': 'none'
    })
    assert operation.created_at == datetime(
        2022, 7, 1, 20, 9, 18, 699628, timezone.utc
    )
    assert operation.updated_at == datetime(
        2022, 7, 1, 20, 9, 18, 699628, timezone.utc
    )
