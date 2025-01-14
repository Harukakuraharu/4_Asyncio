from core.database import initial_db
import asyncio

async def main():
    await initial_db()


if __name__ == "__main__":
    asyncio.run(main())