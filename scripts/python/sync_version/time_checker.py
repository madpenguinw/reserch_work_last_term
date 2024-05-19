import time

import certifi
import requests


def fetch(session, url):
    response = session.get(url)
    return response.text


def main():
    url = "https://habr.com"
    num_requests = 100

    start_time = time.time()

    session = requests.Session()
    session.verify = certifi.where()

    for _ in range(num_requests):
        fetch(session, url)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Время выполнения: {execution_time} секунд")


if __name__ == "__main__":
    main()
