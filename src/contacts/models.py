from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Date, Column, create_engine,Integer
from src.conf.dburl import Config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
import asyncio

engine=create_async_engine(Config.DB_URL)
DBSession=async_sessionmaker(bind=engine)
session=DBSession()
Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id : Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    name : Mapped[str]=mapped_column(String(30))
    surname :Mapped[str]=mapped_column(String(30))
    phone : Mapped[str]=mapped_column(String(30))
    email: Mapped[str]=mapped_column(String(30))
    birthday : Mapped[str]=mapped_column(String(30))
    information: Mapped[str]=mapped_column(String(250))



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Запуск сценария асинхронного создания таблиц
async def main():
    await create_tables()

# Запуск асинхронного сценария
if __name__ == '__main__':
    asyncio.run(main())
