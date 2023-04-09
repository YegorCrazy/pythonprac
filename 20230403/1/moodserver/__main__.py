"""Main moodserver module."""

import asyncio
from .server import Main

if __name__ == '__main__':
    asyncio.run(Main())
