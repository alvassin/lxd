"""
This example can be used to connect using unix socket on host.
"""
import asyncio

from lxd import LXDClient, LXDTransport


async def main():
    async with LXDTransport() as transport:
        client = LXDClient(transport)
        for instance in await client.instances.list():
            print(instance.name)


asyncio.run(main())
