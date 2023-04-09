"""Main moodserver module."""

import asyncio
from .server import Main

if __name__ == '__main__':
    try:
        asyncio.run(Main())
    except KeyboardInterrupt:
        print('Server is down')
