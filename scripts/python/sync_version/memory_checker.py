import time

import certifi
import psutil
import requests


def fetch(session, url):
    response = session.get(url)
    return response.text


def main():
    url = "https://habr.com"
    num_requests = 100

    process = psutil.Process()

    # uss "Unique Set Size" - уникальная для процесса память
    # которая будет освобождена после его закрытия
    memory_usage_before = process.memory_full_info().uss

    session = requests.Session()
    session.verify = certifi.where()

    for _ in range(num_requests):
        fetch(session, url)

    memory_usage_after = process.memory_full_info().uss
    memory_used = (memory_usage_after - memory_usage_before) / 1024 / 1024

    print(f"Использовано памяти: {memory_used} МБ")


if __name__ == "__main__":
    main()
