from datetime import datetime

from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import URL, create_engine, func


class Settings:
	env = Env()
	env.read_env()
	IP: str = env('IP')
	PGUSER: str = env('PGUSER')
	PGPASS: str = env('PGPASS')
	DBNAME: str = env('DBNAME')
	PGHOST: str = env('PGHOST')
	PGPORT: str = env('PGPORT')
	PGHOSTDOCKER: str = env('PGHOSTDOCKER')
	PGPORTDOCKER: str = env('PGPORTDOCKER')

	@property
	def db_url_asyncpg(self):
		return f'postgresql+asyncpg://{self.PGUSER}:{self.PGPASS}@{self.PGHOST}:{self.PGPORT}/{self.DBNAME}'

	def docker_url_asyncpg(self):
		return f'postgresql+asyncpg://{self.PGUSER}:{self.PGPASS}@{self.PGHOSTDOCKER}:{self.PGPORTDOCKER}/{self.DBNAME}'

	@property
	def db_url_psycopg2(self):
		return f'postgresql+psycopg2://{self.PGUSER}:{self.PGPASS}@{self.PGHOST}:{self.PGPORT}/{self.DBNAME}'


settings = Settings()
async_engine = create_async_engine(url=settings.db_url_asyncpg, echo=True, pool_size=5, max_overflow=10)  # это работает ЛОКАЛЬНО
# async_engine = create_async_engine(url=settings.docker_url_asyncpg, echo=True, pool_size=5, max_overflow=10)

sync_engine = create_engine(settings.db_url_psycopg2, echo=True, pool_size=5, max_overflow=10)
sync_session_factory = sessionmaker(sync_engine)  # При запуске выбрать правильный

async_session_factory = async_sessionmaker(async_engine)


class Base(AsyncAttrs, DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True)
	description: Mapped[str] = mapped_column(nullable=True)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())

	repr_cols_num = 3  # количество колонок в выводе в принт
	repr_cols = tuple()  # Всё это можно переопределить для подчинённого класса

	def __repr__(self):  # Модифицируем вывод в принт, когда запросы делаем
		"""relationship() не используются в repr. тк могут привести к неожиданным подгрузкам"""
		cols = [f"{col}={getattr(self, col)}" for idx, col in enumerate(self.__table__.columns.keys()) if
				col in self.repr_cols or idx < self.repr_cols_num]

		return f"<{self.__class__.__name__} | {', '.join(cols)} >"
