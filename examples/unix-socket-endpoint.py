"""
This example can be used to list instances using unix socket.
"""
import asyncio
import os

from lxd import LXDClient, LXDTransport


async def list_instances(transport: LXDTransport):
    client = LXDClient(transport)
    for instance in await client.instances.list():
        print(instance.name)


async def main():
    # Use default unix socket path
    async with LXDTransport() as transport:
        await list_instances(transport)

    # Use specific path to unix socket
    async with LXDTransport(
        endpoint_url='unix:///directory/unix.socket'
    ) as transport:
        await list_instances(transport)

    # Use LXD_DIR environment variable
    # (would use /directory/unix.socket as path in this case)
    os.environ['LXD_DIR'] = '/directory'
    async with LXDTransport() as transport:
        await list_instances(transport)


asyncio.run(main())
