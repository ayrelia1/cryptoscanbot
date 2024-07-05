from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import os


sqlalchemy_url = f"postgresql+asyncpg://{os.environ.get('DB_LOG')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"

engine = create_async_engine(sqlalchemy_url)

async_session = async_sessionmaker(engine)




