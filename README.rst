Async python client for `LXD REST API`_ (currently under heavy development).

.. _LXD REST API: https://linuxcontainers.org/lxd/api/master/#/

.. contents::


Usage
=====

Installation
------------

.. code-block:: shell

    pip install lxd


Initialize client
-----------------
.. code-block:: python

    import asyncio
    from pathlib import Path

    from lxd import LXDTransport, LXDClient


    async def main():
        async with LXDTransport(
            endpoint_url='https://mylxd:8443/',
            cert_path=Path('~/.config/lxc/client.crt'),
            key_path=Path('~/.config/lxc/client.key'),
            endpoint_cert_path=Path('~/.config/lxc/servercerts/mylxd.crt'),
        ) as transport:
            client = LXDClient(transport)
            await client.authenticate(
                cert_path=Path('~/.config/lxc/client.crt'),
                password='your-trust-password'
            )


    asyncio.run(main())

Example usages
--------------
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
---------------------
.. code-block:: python

    from lxd.entities.instances import InstanceAction

    instances = await client.instances.list()
    operation = await client.instances.update_state(
        instances[0].name, action=InstanceAction.STOP
    )
    await client.operations.wait(operation.id)  # wait as long as possible
    await client.operations.wait(operation.id, timeout=30)  # 30s


Get event stream
----------------
.. code-block:: python

    async for event in client.server.get_events():
        # See Event object for more properties
        print(event.type)
        print(event.metadata)


Available Endpoints
===================

Server
------

server.get
~~~~~~~~~~
Get server environment and configuration.

.. code-block:: python

    # See lxd.entities.server.Server
    info = await client.server.get()
    print(info.config)
    print(info.environment)


server.update_configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Update the entire `server configuration <https://linuxcontainers.org/lxd/docs/master/server/>`_.

.. code-block:: python

    await client.server.update_configuration({
        'core.https_address': '0.0.0.0:8443'
        'core.trust_password': 'very-strong-password'
    })


You may need to send ``int`` values as ``str``, otherwise lxd would not be able to parse them:

.. code-block:: python

    await client.server.update_configuration({
        # 2 (int) value would cause error:
        # 'cannot set \'images.remote_cache_expiry\': invalid type float64'
        'images.remote_cache_expiry': '2'
    })


server.update_configuration_subset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Update a subset of the `server configuration <https://linuxcontainers.org/lxd/docs/master/server/>`_.

.. code-block:: python

    await client.server.update_configuration_subset({
        'core.trust_password': 'very-strong-password'
    })


You may need to send ``int`` values as ``str``, otherwise lxd would not be able to parse them:

.. code-block:: python

    await client.server.update_configuration({
        # 2 (int) value would cause error:
        # 'cannot set \'images.remote_cache_expiry\': invalid type float64'
        'images.remote_cache_expiry': '2'
    })


server.get_resources
~~~~~~~~~~~~~~~~~~~~
Gets the hardware information profile of the LXD server.

.. code-block:: python

    # See lxd.entities.server.ServerResources
    server_resources = await client.server.get_resources()
    print(server_resources.cpu)


server.get_events
~~~~~~~~~~~~~~~~~
Connect to `event API <https://linuxcontainers.org/lxd/docs/master/events/>`_
using websocket.

.. code-block:: python

    # Listen all events
    async for event in client.server.get_events():
        print(event.type)
        print(event.metadata)

    # Listen to specific events
    async for event in client.server.get_events(type='operation'):
        print(event.metadata.id)
        print(event.metadata.status)


Certificates
------------
certificates.list
~~~~~~~~~~~~~~~~~

Returns a list of trusted certificates.

.. code-block:: python

    # See lxd.entities.certificates.Certificate
    certs = await client.certificates.list()
    print(certs[0].fingerprint)


If you pass ``recursion=0`` parameter, lxd would return just references,
which are represented in current module as
``lxd.entities.certificates.CertificateLink`` objects.

If you ``await`` such link object - you would get object itself (separate http
request is performed for every await call).

.. code-block:: python

    cert_links = await client.certificates.list(recursion=0)
    certs = await asyncio.gather(*cert_links)


certificates.get
~~~~~~~~~~~~~~~~

Gets a specific certificate entry from the trust store by fingerprint.

.. code-block:: python

    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.primitives import hashes

    fprint = '97f267c0fe20fd013b6b4ba3f5440ea3e9361ce8568d41c633f28c620ab37ea0'
    cert = await client.certificates.get(fprint)

    cert_obj = load_pem_x509_certificate(cert.certificate.encode())
    assert cert_obj.fingerprint(hashes.SHA256()).hex() == fprint


certificates.add
~~~~~~~~~~~~~~~~

Adds a certificate to the trust store as trusted user (client certificate
should be trusted).

.. code-block:: python

    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    subj = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "alvassin@osx")
    ])

    cert = x509.CertificateBuilder().subject_name(
        subj
    ).issuer_name(
        subj
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    await client.certificates.add(
        cert.public_bytes(serialization.Encoding.PEM)
    )


If ``password`` argument is specified, adds a certificate to the trust store
as an untrusted user.

.. code-block:: python

    await client.certificates.add(
        cert.public_bytes(serialization.Encoding.PEM),
        password='your-trust-password'
    )


certificates.update_configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update the entire certificate configuration.

.. code-block:: python

    await client.certificates.update_configuration(
        '97f267c0fe20fd013b6b4ba3f5440ea3e9361ce8568d41c633f28c620ab37ea0',
        certificate='-----BEGIN CERTIFICATE-----\n...',
        name='new-name',
        projects=[],
        restricted=False,
        type='client'
    )


certificates.update_configuration_subset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update a subset of the certificate configuration.

.. code-block:: python

    await client.certificates.update_configuration_subset(
        '97f267c0fe20fd013b6b4ba3f5440ea3e9361ce8568d41c633f28c620ab37ea0',
        name='another-name'
    )

certificates.remove
~~~~~~~~~~~~~~~~~~~

Removes the certificate from the trust store.

.. code-block:: python

    await client.certificates.remove(
        '97f267c0fe20fd013b6b4ba3f5440ea3e9361ce8568d41c633f28c620ab37ea0'
    )


Instances
---------
instances.list
~~~~~~~~~~~~~~

Get instances list.

instances.get
~~~~~~~~~~~~~

Get a specific instance (basic struct).

instances.create
~~~~~~~~~~~~~~~~

Create a new instance on LXD.

Depending on the source, this can create an instance from an existing
local image, remote image, existing local instance or snapshot, remote
migration stream or backup file.

instances.delete
~~~~~~~~~~~~~~~~

Deletes a specific instance and anything owned by the instance,
such as snapshots and backups.

instances.get_state
~~~~~~~~~~~~~~~~~~~

Gets the runtime state of the instance.

This is a reasonably expensive call as it causes code to be run
inside of the instance to retrieve the resource usage and network
information.

instances.update_state
~~~~~~~~~~~~~~~~~~~~~~

Changes the running state of the instance.

Operations
----------
operations.list
~~~~~~~~~~~~~~~
Get a list of operations.

operations.get
~~~~~~~~~~~~~~
Get specific operation state.

operations.wait
~~~~~~~~~~~~~~~

Wait for the operation to reach a final state (or timeout)
and retrieve its final state.

operations.cancel
~~~~~~~~~~~~~~~~~

Cancel the operation (if supported by operation).

TODO
====
* Add `filtering support`_.

.. _filtering support: https://linuxcontainers.org/lxd/docs/master/rest-api/#filtering
