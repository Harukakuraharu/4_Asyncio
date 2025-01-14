import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models import models


class BaseCrud:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = models.SpimexTradingResults

    async def create_item(self, data: list):
        stmt = sa.insert(self.model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
