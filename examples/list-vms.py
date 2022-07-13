import asyncio
from argparse import ArgumentParser
from pathlib import Path

from lxd import make_client
from yarl import URL


parser = ArgumentParser()
parser.add_argument('--endpoint-url', type=URL, required=True)
parser.add_argument(
    '--cert-path', type=Path, default=Path('~/.config/lxc/client.crt')
)
parser.add_argument(
    '--key-path', type=Path, default=Path('~/.config/lxc/client.key')
)
parser.add_argument('--endpoint-cert-path', type=Path)


async def main():
    args = parser.parse_args()
    async with make_client(
        endpoint_url=args.endpoint_url,
        cert_path=args.cert_path,
        key_path=args.key_path,
        endpoint_cert_path=args.endpoint_cert_path
    ) as lxd_client:
        for instance in await lxd_client.instances.list():
            print(instance.name)


asyncio.run(main())
