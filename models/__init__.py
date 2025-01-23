from typing import Type, TypeVar

from models.models import Base, SpimexTradingResults


MODEL = TypeVar("MODEL", bound=Base)

TypeModel = Type[MODEL]
