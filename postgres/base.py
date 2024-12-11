from enum import Enum
from decimal import Decimal
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, class_mapper
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()
    metadata = MetaData(schema='public')
    alias = {}

    def to_dict(self) -> dict:
        result = {}
        for column in class_mapper(self.__class__).columns:
            value = getattr(self, column.key)
            if isinstance(value, Enum):
                value = value.value
            elif isinstance(value, Decimal):
                value = float(value)

            if self.alias.get(column.key) is not None:
                result[self.alias[column.key]] = value
            else:
                result[column.key] = value

        return result

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__}: {', '.join(cols)}>"


class AsyncPostgreSQLClient:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url, echo=echo)
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(self.engine,
                                                                                   expire_on_commit=False,
                                                                                   autocommit=False)
        self._factory = async_scoped_session(self._session_maker, scopefunc=current_task)

    async def init_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def create_selected_table(self, table):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, [table])

    async def drop_selected_table(self, table):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all, [table])

    @asynccontextmanager
    async def __call__(self) -> AsyncSession:  # type: ignore
        try:
            async with self._factory() as s:
                yield s
        finally:
            await self._factory.remove()
