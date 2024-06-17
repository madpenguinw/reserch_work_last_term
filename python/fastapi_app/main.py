import json
from contextlib import asynccontextmanager

import aiofiles
from aiocache import cached  # noqa
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from psycopg2 import connect, pool
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from models import User

app = FastAPI()

# PostgreSQL configurations
PG_CONN_STRING = (
    "dbname='VKR' user='admin' password='12345678' "
    "host='localhost' port='1234'"
)
POSTGRES_URL = "postgresql+asyncpg://admin:12345678@localhost:1234/VKR"
POSTGRES_URL_ASYNCPG = "postgresql://admin:12345678@localhost:1234/VKR"
connection_pool = pool.SimpleConnectionPool(1, 40, PG_CONN_STRING)


# SQLAlchemy setup
engine = create_async_engine(
    POSTGRES_URL,
    echo=True,
    pool_size=20,
    max_overflow=20,
)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()
        connection_pool.closeall()


app.router.lifespan_context = lifespan


@app.get("/empty", tags=["Base"])
async def get_empty():
    return []


@app.get("/readfile/sync/{filename}", tags=["Base"])
async def read_file_sync(filename: str):
    with open(f"./{filename}", "r") as f:
        data = json.load(f)
    return JSONResponse(data)


@cached(ttl=300)  # Кэширование на 5 минут
async def get_file_content(filename: str):
    async with aiofiles.open(f"./{filename}", "r") as f:
        data = await f.read()
        return json.loads(data)


@app.get("/readfile/async/{filename}", tags=["Base"])
async def read_file_async(filename: str):
    json_data = await get_file_content(filename)
    return JSONResponse(json_data)


@app.get("/postgres/get_users_sqlalchemy_select/{count}", tags=["Postgres"])
async def get_users_sqlalchemy_select(count: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).limit(count))
        users = result.scalars().all()
        users_dict = [user.to_dict() for user in users]
        return JSONResponse(content=users_dict)


@app.get("/postgres/get_users_sqlalchemy_text/{count}", tags=["Postgres"])
async def get_users_sqlalchemy_text(count: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text(f"SELECT * FROM users LIMIT {count}")
        )
        users = result.scalars().all()
        users_dict = [user.to_dict() for user in users]
        return JSONResponse(content=users_dict)


@app.get("/postgres/get_users_psycopg2/{count}", tags=["Postgres"])
async def get_users_psycopg2(count: int):
    with connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM users LIMIT {count}")
            users = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
    return JSONResponse([dict(zip(columns, row)) for row in users])


@app.get("/postgres/get_users_psycopg2_pool/{count}", tags=["Postgres"])
async def get_users_psycopg2_pool(count: int):
    conn = connection_pool.getconn()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users LIMIT %s", (count,))
        users = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    connection_pool.putconn(conn)
    return JSONResponse([dict(zip(columns, row)) for row in users])


@app.post("/postgres/populate", tags=["Upload to DB"])
async def populate_postgres_sql():
    with open("data.json", "r") as f:
        data = json.load(f)
    query = """
        INSERT INTO users (firstname, lastname, patronymic, age)
        VALUES (%s, %s, %s, %s)
    """
    with connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            for user in data:
                cur.execute(
                    query,
                    (
                        user["firstname"],
                        user["lastname"],
                        user["patronymic"],
                        user["age"],
                    ),
                )
    return {"status": "success"}
