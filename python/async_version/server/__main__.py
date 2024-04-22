import asyncio

from server.main import run_app

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_app())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
