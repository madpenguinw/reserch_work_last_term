import asyncpg
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# PostgreSQL configurations
POSTGRES_URL = "postgresql://admin:12345678@localhost:1234/VKR"


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(dsn=POSTGRES_URL)


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


async def get_connection():
    async with app.state.pool.acquire() as connection:
        yield connection


@app.get("/postgres/get_users_asyncpg/{count}", tags=["Postgres"])
async def get_users_asyncpg(count: int, connection=Depends(get_connection)):
    query = "SELECT * FROM users LIMIT $1"
    users = await connection.fetch(query, count)
    return JSONResponse([dict(user) for user in users])
