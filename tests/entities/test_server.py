from datetime import datetime, timezone

from lxd.entities.operations import Operation
from lxd.entities.server import Event, LifecycleEvent, LoggingEvent


def test_create_logging_event():
    event = Event.from_dict({
        'type': 'logging',
        'timestamp': '2022-07-08T14:29:41.602652413Z',
        'metadata': {
            'message': 'Event listener server handler started',
            'level': 'debug',
            'context': {
                'id': '6d620d0b-91ab-46a5-9da7-49fcb45e235a',
                'local': '127.0.0.1:8443',
                'remote': '127.0.0.1:64555'
            }
        },
        'location': 'none'
    })
    assert isinstance(event.metadata, LoggingEvent)
    assert event.timestamp == datetime(
        2022, 7, 8, 14, 29, 41, 602652, timezone.utc
    )


def test_create_operation_event():
    event = Event.from_dict({
        'type': 'operation',
        'timestamp': '2022-07-08T15:34:06.766796314Z',
        'metadata': {
            'id': '52bc121d-d5e5-4c39-850a-af421984d345',
            'class': 'task',
            'description': 'Stopping instance',
            'created_at': '2022-07-08T15:34:06.762246839Z',
            'updated_at': '2022-07-08T15:34:06.762246839Z',
            'status': 'Pending',
            'status_code': 105,
            'resources': {
                'instances': ['/1.0/instances/deciding-yeti']
            },
            'metadata': None,
            'may_cancel': False,
            'err': '',
            'location': 'none'
        },
        'location': 'none',
        'project': 'default'
    })
    assert isinstance(event.metadata, Operation)
    assert event.timestamp == datetime(
        2022, 7, 8, 15, 34, 6, 766796, timezone.utc
    )


def test_create_lifecycle_event():
    event = Event.from_dict({
        'type': 'lifecycle',
        'timestamp': '2022-07-08T15:34:08.546278023Z',
        'metadata': {
            'action': 'instance-shutdown',
            'source': '/1.0/instances/deciding-yeti',
            'requestor': {
                'username': (
                    '97f267c0fe20fd013b6b4ba3f5440ea3e9361ce8568d41c633f28c620'
                    'ab37ea0'
                ),
                'protocol': 'tls',
                'address': '127.0.0.1:50393'
            }
        },
        'location': 'none',
        'project': 'default'
    })
    assert isinstance(event.metadata, LifecycleEvent)
    assert event.timestamp == datetime(
        2022, 7, 8, 15, 34, 8, 546278, timezone.utc
    )
