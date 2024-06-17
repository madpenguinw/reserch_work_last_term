import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import chain, combinations

import numpy as np
from aiohttp import web

from server.constants import BAD_REQUEST
from server.logger import custom_logger


class SubsetSumHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def get_subsets_handler(self, request):
        start_time = datetime.now()

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

        response_data = {
            "Service": "Python Async Version",
            "Result": result,
            "Time_ms": int(
                (datetime.now() - start_time).total_seconds() * 1000
            ),
        }
        custom_logger.info(response_data)

        return web.json_response(response_data)

    async def get_subsets_numpy_handler(self, request):
        start_time = datetime.now()

        try:
            query_params = request.rel_url.query
            sum_value = int(query_params["sum"])
            query_data = json.loads(query_params["data"])
        except (ValueError, json.JSONDecodeError, KeyError):
            custom_logger.error(BAD_REQUEST)
            return web.Response(status=400, text=BAD_REQUEST)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor, self.solve_subset_sum_numpy, query_data, sum_value
        )

        response_data = {
            "Service": "Python Async Version with Numpy",
            "Result": result,
            "Time_ms": int(
                (datetime.now() - start_time).total_seconds() * 1000
            ),
        }
        custom_logger.info(response_data)

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

    def solve_subset_sum_numpy(self, data, target_sum):
        data = np.array(data)
        all_subsets = list(
            chain.from_iterable(
                combinations(data, r) for r in range(len(data) + 1)
            )
        )

        result_subsets = [
            list(subset)
            for subset in all_subsets
            if np.sum(subset) == target_sum
        ]

        length_result_subsets = len(result_subsets)
        custom_logger.info(length_result_subsets)
        return length_result_subsets
