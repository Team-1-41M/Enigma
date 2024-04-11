import asyncio
import sys

from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        async with session.ws_connect(
            f"http://127.0.0.1:8000/api/v1/projects/{sys.argv[1]}/content"
        ) as ws:
            loop = asyncio.get_event_loop()

            async def send_data():
                while True:
                    data = await loop.run_in_executor(None, input, "")
                    await ws.send_str(data)

            async def receive_data():
                while True:
                    msg = await ws.receive_str()
                    print(msg)

            await asyncio.gather(send_data(), receive_data())


asyncio.run(main())
