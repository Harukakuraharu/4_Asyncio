import os
from dataclasses import dataclass, field
from typing import Any

import aiohttp
import pandas as pd

from core.database import async_session
from crud import crud


@dataclass
class FileDownloader:
    """Class for work with file - download and delete"""

    async def initial_download(self, current_date):
        url = f"https://spimex.com/upload/reports/oil_xls/oil_xls_{current_date}162000.xls?r=9455"
        filename = f"{current_date}.xls"
        await self.download_file(url, filename)
        try:
            await FileParser(filename).insert_to_db()
            print(f"Data save in database for {current_date}")
            self.delete_file(filename)
        except FileNotFoundError:
            pass

    async def download_file(self, url, filename: str) -> tuple[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(filename, "wb") as f:
                        f.write(content)

    def delete_file(self, filename: str) -> None:
        if os.path.exists(filename):
            os.remove(filename)


@dataclass
class FileParser:

    filename: str
    data: list = field(default_factory=pd.DataFrame)
    async_session = async_session

    async def get_data(self, filename):
        data = pd.read_excel(filename)
        return data

    async def update_table(self):
        self.data = await self.get_data(self.filename)
        date_data = self.data["Форма СЭТ-БТ"].iloc[2].split(": ")
        self.data.columns = list(range(15))
        self.data = self.data[[1, 2, 3, 4, 5, 14]][self.data[14] != "-"].dropna()
        self.data.drop(5, inplace=True)
        return date_data[-1]

    async def make_data_list(self, date_data: str) -> list:
        return [
            {
                "exchange_product_id": row[1],
                "exchange_product_name": row[2],
                "oil_id": row[1][:4],
                "delivery_basis_id": row[1][4:7],
                "delivery_basis_name": row[3],
                "delivery_type_id": row[1][-1],
                "volume": row[4],
                "total": row[5],
                "count": row[14],
                "date": date_data,
            }
            for _, row in self.data.iterrows()
        ]

    async def insert_to_db(self) -> None:
        async with self.async_session() as session:
            date_current = await self.update_table()
            data = await self.make_data_list(date_current)
            await crud.BaseCrud(session).create_item(data)
            await session.commit()
