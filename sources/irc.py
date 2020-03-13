# -*- coding: utf-8 -*-
import asyncio
import logging
import re

from settings import NICK, OAUTH

LOG = logging.getLogger(__name__)
connected_to = {}


async def send_credentials(websocket):
    await websocket.send('PASS {}\r\n'.format(OAUTH))
    await websocket.send('NICK {}\r\n'.format(NICK))


async def send_pong(websocket):
    await websocket.send('PONG :tmi.twitch.tv\r\n')
    LOG.info('Sent PONG')


async def join_channels(websocket, channels):
    for channel in channels:
        # sleep to make sure we won't exceed 50/15 limit
        await asyncio.sleep(0.4)
        await websocket.send('JOIN #{}\r\n'.format(channel[1]))
        connected_to[channel[0]] = channel[1]
        LOG.info(f'Joined {channel[1]}')


async def part_channels(websocket, channels):
    for channel in channels:
        # sleep to make sure we won't exceed 50/15 limit
        await asyncio.sleep(0.4)
        await websocket.send('PART #{}\r\n'.format(channel[1]))
        del connected_to[channel[0]]
        LOG.info(f'Parted {channel[1]}')


async def read_info(websocket):
    prev_data = ''
    while True:
        try:
            data = await websocket.recv()
            if 'PING :tmi.twitch.tv' in prev_data + data:
                await send_pong(websocket)
            messages = re.split(r'[~\r\n]+', prev_data + data)
            # for msg in messages:
            #     print(msg)
            prev_data = messages[-1]
        except Exception as exc:
            LOG.exception(exc)
            raise
