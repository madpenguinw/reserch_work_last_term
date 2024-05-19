import json
from contextlib import asynccontextmanager

import psycopg2
from fastapi import FastAPI, HTTPException
from mongoengine import Document, IntField, StringField, connect
from pymongo import MongoClient
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import database
from models import User

app = FastAPI()

# PostgreSQL configurations
PG_CONN_STRING = (
    "dbname='VKR' user='admin' password='12345678' "
    "host='localhost' port='1234'"
)
POSTGRES_URL = (
    "postgresql+asyncpg://admin:12345678@localhost:1234/VKR"
)

# MongoDB configurations
MONGO_URL = "mongodb://admin:12345678@localhost:3456"
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["VKR"]
mongo_users_collection = mongo_db["users"]

# MongoEngine setup
connect(db="VKR", host=MONGO_URL)

# SQLAlchemy setup
engine = create_async_engine(POSTGRES_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    await engine.dispose()


app.router.lifespan_context = lifespan


# MongoEngine model
class MongoUser(Document):
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    patronymic = StringField(required=True)
    age = IntField(required=True)

    meta = {"collection": "users"}


# Endpoints
@app.get("/empty", tags=["Base"])
async def get_empty():
    return []


@app.get("/readfile/{filename}", tags=["Base"])
async def read_file(filename: str):
    try:
        with open(f"./{filename}", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/mongo/get_users_odm/{count}", tags=["Mongo"])
async def get_users_odm(count: int):
    employees = (
        MongoUser.objects.limit(count) if count else MongoUser.objects.all()
    )
    employees_data = [
        {
            "_id": str(employee.id),
            "firstname": employee.firstname,
            "patronymic": employee.patronymic,
            "lastname": employee.lastname,
            "age": employee.age,
        }
        for employee in employees
    ]
    return employees_data


@app.get("/mongo/get_users/{count}", tags=["Mongo"])
async def get_users_driver(count: int):
    users = list(mongo_users_collection.find().limit(count))
    for user in users:
        user["_id"] = str(user["_id"])
    return users


@app.get("/postgres/get_users_orm/{count}", tags=["Postgres"])
async def get_users_orm(count: int):
    async with AsyncSessionLocal() as session:
        query = select(User).limit(count)
        result = await session.execute(query)
    users = result.fetchall()
    user_dicts = [dict(zip(result.keys(), user)) for user in users]

    return user_dicts


@app.get("/postgres/get_users_orm_text/{count}", tags=["Postgres"])
async def get_users_orm_text(count: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text(f"SELECT * FROM users LIMIT {count}")
        )
        users = result.fetchall()
    user_dicts = [dict(zip(result.keys(), user)) for user in users]

    return user_dicts


@app.get("/postgres/get_users/{count}", tags=["Postgres"])
async def get_users_sql(count: int):
    with psycopg2.connect(PG_CONN_STRING) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM users LIMIT {count}")
            users = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            result = [dict(zip(columns, row)) for row in users]
    return result


@app.post("/mongo/populate", tags=["Upload to DB"])
async def populate_mongo():
    with open("data.json", "r") as f:
        data = json.load(f)
    mongo_users_collection.insert_many(data)
    return {"status": "success"}


@app.post("/mongo/populate_odm", tags=["Upload to DB"])
async def populate_mongo_odm():
    with open("data.json", "r") as f:
        data = json.load(f)
    for user in data:
        MongoUser(**user).save()
    return {"status": "success"}


@app.post("/postgres/populate_orm", tags=["Upload to DB"])
async def populate_postgres():
    with open("data.json", "r") as f:
        data = json.load(f)
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add_all([User(**user) for user in data])
    return {"status": "success"}


@app.post("/postgres/populate", tags=["Upload to DB"])
async def populate_postgres_sql():
    with open("data.json", "r") as f:
        data = json.load(f)
    query = """
        INSERT INTO users (firstname, lastname, patronymic, age)
        VALUES (%s, %s, %s, %s)
    """
    with psycopg2.connect(PG_CONN_STRING) as conn:
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
