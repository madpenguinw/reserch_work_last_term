import asyncio
import ssl

import aiohttp
import certifi
import psutil


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    url = "https://habr.com"
    num_requests = 100

    process = psutil.Process()

    # uss "Unique Set Size" - уникальная для процесса память
    # которая будет освобождена после его закрытия
    memory_usage_before = process.memory_full_info().uss

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        tasks = [fetch(session, url) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

    memory_usage_after = process.memory_full_info().uss
    memory_used = (memory_usage_after - memory_usage_before) / 1024 / 1024

    print(f"Использовано памяти: {memory_used} МБ")


if __name__ == "__main__":
    asyncio.run(main())
