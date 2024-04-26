import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import chain, combinations

from aiohttp import web

from server.constants import BAD_REQUEST
from server.logger import custom_logger


class SubsetSumHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def get_subsets_handler(self, request):
        start_time = round(time.time() * 1000, 3)

        try:
            query_params = request.rel_url.query
            sum_value = int(query_params["sum"])
            query_data = json.loads(query_params["data"])
        except (ValueError, json.JSONDecodeError, KeyError):
            custom_logger.error(BAD_REQUEST)
            return web.Response(status=400, text=BAD_REQUEST)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor, self.solve_subset_sum, query_data, sum_value
        )

        end_time = round(time.time() * 1000, 3)
        delta_time = round(end_time - start_time, 3)
        response_data = {
            "Service": "Python Async Version",
            "Result": result,
            "Time": f"{delta_time}ms",
        }
        custom_logger.info(f"Request Processing Time: {delta_time}ms")

        return web.json_response(response_data)

    def solve_subset_sum(self, data, target_sum):
        all_subsets = list(
            chain.from_iterable(
                combinations(data, r) for r in range(len(data) + 1)
            )
        )
        result_subsets = [
            list(subset)
            for subset in all_subsets
            if subset and sum(subset) == target_sum
        ]
        length_result_subsets = len(result_subsets)
        custom_logger.info(length_result_subsets)
        return length_result_subsets
