import asyncio
from datetime import date, datetime, timedelta

from aiohttp import ClientSession
from more_itertools import chunked

from core.database import initial_db
from utils import utils


async def main():
    session = ClientSession()
    await initial_db()
    date_start = date(2023, 1, 1)
    date_end = date.today()
    delta = date_end - date_start
    await asyncio.sleep(0.5)
    for day in chunked(range(delta.days + 1), 5):
        current_date = [
            (date_start + timedelta(days=time)).strftime("%Y%m%d") for time in day
        ]
        tasks = [utils.FileDownloader().initial_download(time) for time in current_date]
        await asyncio.gather(*tasks)
    await session.close()


if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(main())
    print(f"Время загрузки данных - {datetime.now() - start} ")
