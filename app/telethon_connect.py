import asyncio

from telethon import TelegramClient
from app.core.config import settings


async def main():
    client = TelegramClient(
        session=f"boost_{settings.API_ID}",
        api_id=settings.API_ID,
        api_hash=settings.API_HASH
    )
    await client.start(phone=settings.PHONE)


if __name__ == "__main__":
    asyncio.run(main())