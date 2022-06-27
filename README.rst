Installation
------------

.. code-block:: shell

    pip install lxd


Usage
-----

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
