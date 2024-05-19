import asyncio
import ssl
import time

import aiohttp
import certifi


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    url = "https://habr.com"
    num_requests = 100

    start_time = time.time()

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        tasks = [fetch(session, url) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Время выполнения: {execution_time} секунд")


if __name__ == "__main__":
    asyncio.run(main())
