import asyncio

import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB configuration
MONGO_URL = "mongodb://admin:12345678@localhost:3456"

# PostgreSQL configuration
POSTGRES_URL = "postgresql://admin:12345678@localhost:1234/VKR"


async def get_mongodb_version():
    mongo_client = AsyncIOMotorClient(MONGO_URL)
    server_info = await mongo_client.server_info()
    return server_info["version"]


async def get_postgresql_version():
    conn = await asyncpg.connect(POSTGRES_URL)
    version = await conn.fetchval("SELECT version()")
    await conn.close()
    return version


async def main():
    mongodb_version = await get_mongodb_version()
    postgresql_version = await get_postgresql_version()

    print(f"MongoDB version: {mongodb_version}")
    print(f"PostgreSQL version: {postgresql_version}")


if __name__ == "__main__":
    asyncio.run(main())
