# -*- coding: utf-8 -*-
import asyncio
import logging
import websockets

from settings import HOST, LOG_LEVEL, PORT

from sources.irc import read_info, send_credentials
from sources.new_api import idle


logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


async def run():
    async with websockets.connect(f'{HOST}:{PORT}') as websocket:
        await send_credentials(websocket)

        try:
            await asyncio.gather(
                read_info(websocket),
                idle(websocket),
            )
        except websockets.ConnectionClosed:
            websocket = websockets.connect(f'{HOST}:{PORT}')


if __name__ == '__main__':
    asyncio.run(run())
