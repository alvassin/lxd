from datetime import datetime, timezone

from lxd.entities.instances import Instance


def test_create_instance():
    instance = Instance.from_dict({
        'architecture': 'x86_64',
        'config': {
            'image.architecture': 'amd64',
            'image.description': 'ubuntu 22.04 LTS amd64 (release) (20220622)',
            'image.label': 'release',
            'image.os': 'ubuntu',
            'image.release': 'jammy',
            'image.serial': '20220622',
            'image.type': 'squashfs',
            'image.version': '22.04',
            'volatile.base_image': (
                'a0d7bbb3756a64f56d17797535ef6641c73e69540defa0bd6b07b09f31525'
                '7b4'
            ),
            'volatile.cloud-init.instance-id': (
                '8ff627e9-b19b-4a27-a10b-624f51a3217c'
            ),
            'volatile.eth0.hwaddr': '00:16:3e:23:0b:66',
            'volatile.idmap.base': '0',
            'volatile.idmap.current': '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]',
            'volatile.idmap.next': '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]',
            'volatile.last_state.idmap': '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]',
            'volatile.last_state.power': 'STOPPED',
            'volatile.uuid': 'eac157c3-77f5-4956-b646-a27f0850c4b4'
        },
        'devices': {},
        'ephemeral': False,
        'profiles': ['default'],
        'stateful': False,
        'description': '',
        'expanded_config': {
            'image.architecture': 'amd64',
            'image.description': 'ubuntu 22.04 LTS amd64 (release) (20220622)',
            'image.label': 'release',
            'image.os': 'ubuntu',
            'image.release': 'jammy',
            'image.serial': '20220622',
            'image.type': 'squashfs',
            'image.version': '22.04',
            'volatile.base_image': 'a0d7bbb3756a64f56d17797535ef6641c73e69540defa0bd6b07b09f315257b4',
            'volatile.cloud-init.instance-id': '8ff627e9-b19b-4a27-a10b-624f51a3217c',
            'volatile.eth0.hwaddr': '00:16:3e:23:0b:66',
            'volatile.idmap.base': '0',
            'volatile.idmap.current': '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]',
            'volatile.idmap.next': '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]',
            'volatile.last_state.idmap': '[{"Isuid":true,"Isgid":false,"Hostid":1000000,"Nsid":0,"Maprange":1000000000},{"Isuid":false,"Isgid":true,"Hostid":1000000,"Nsid":0,"Maprange":1000000000}]',
            'volatile.last_state.power': 'STOPPED',
            'volatile.uuid': 'eac157c3-77f5-4956-b646-a27f0850c4b4'
        },
        'expanded_devices': {
            'eth0': {
                'name': 'eth0',
                'network': 'lxdbr0',
                'type': 'nic'
            },
            'root': {
                'path': '/',
                'pool': 'default',
                'type': 'disk'
            }
        },
        'name': 'deciding-yeti',
        'status': 'Stopped',
        'status_code': 102,
        'created_at': '2022-06-28T21:03:34.195869823Z',
        'last_used_at': '2022-07-08T14:10:47.431529387Z',
        'location': 'none',
        'type': 'container',
        'project': 'default'
    })
    assert instance.created_at == datetime(
        2022, 6, 28, 21, 3, 34, 195869, timezone.utc
    )
