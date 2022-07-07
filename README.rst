Async python client for `LXD REST API`_ (currently under heavy development).

.. _LXD REST API: https://linuxcontainers.org/lxd/api/master/#/

Usage
-----

Installation
~~~~~~~~~~~~

.. code-block:: shell

    pip install lxd


Initialize client
~~~~~~~~~~~~~~~~~
.. code-block:: python

    import asyncio
    from pathlib import Path

    from yarl import URL

    from lxd.client import lxd_client


    async def main():
        client = lxd_client(
            URL('https://mylxd:8443/'),
            cert_path=Path('~/.config/lxc/client.crt'),
            key_path=Path('~/.config/lxc/client.key'),
            endpoint_cert_path=Path('~/.config/lxc/servercerts/mylxd.crt'),
        )

        await client.authenticate(
            cert_path=Path('~/.config/lxc/client.crt'),
            password='your-trust-password'
        )


    asyncio.run(main())

Example usages
~~~~~~~~~~~~~~
.. code-block:: python

    # Recursion 0 returns only links to objects,
    # you can resolve them by awaiting
    instance_links = await client.instances.list(recursion=0)
    instance = await instance_links[0]

    # Recursion 1 returns only some fields
    instances = await client.instances.list(recursion=1)

    # Recursion 2 returns all possible information
    instances = await client.instances.list(recursion=2)


Change instance state
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from lxd.entities.instances import InstanceAction

    instances = await client.instances.list()
    operation = await client.instances.update_state(
        instances[0].name, action=InstanceAction.STOP
    )
    await client.operations.wait(operation.id)  # wait as long as possible
    await client.operations.wait(operation.id, timeout=30)  # 30s


Available Endpoints
-------------------

Server
~~~~~~
* client.server.get
* client.server.get_resources
* client.update_configuration
* client.partial_update_configuration

Certificates
~~~~~~~~~~~~
* client.certificates.list
* client.certificates.add
* client.certificates.get
* client.certificates.update
* client.certificates.partial_update
* client.certificates.delete

Instances
~~~~~~~~~
* client.instances.list
* client.instances.get
* client.instances.create
* client.instances.delete
* client.instances.get_state
* client.instances.update_state

Operations
~~~~~~~~~~
* client.operations.list
* client.operations.get
* client.operations.wait
* client.operations.cancel
