import os

from aiohttp import web

from server.logger import custom_logger, log_middleware
from server.logic import SubsetSumHandler


async def run_app():
    app = web.Application(middlewares=[log_middleware])
    handler = SubsetSumHandler()

    app.router.add_get("/getSubsets", handler.get_subsets_handler)
    app.router.add_get("/getSubsetsNumpy", handler.get_subsets_numpy_handler)
    app.router.add_route(
        "*",
        "/{path:.*}",
        lambda r: web.Response(text="Successful!", status=200),
    )

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    custom_logger.info(f"Started server on {host}:{port}")
