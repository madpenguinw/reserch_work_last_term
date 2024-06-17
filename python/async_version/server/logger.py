import logging

from aiohttp.web_middlewares import middleware

custom_logger = logging.getLogger("custom_logger")
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s " "%(funcName)s: %(message)s")
stream_handler.setFormatter(formatter)
custom_logger.addHandler(stream_handler)

custom_logger.setLevel(logging.DEBUG)


@middleware
async def log_middleware(request, handler):
    response = await handler(request)
    custom_logger.info(
        f"{request.method} {str(request.url)} {response.status}",
    )
    return response
