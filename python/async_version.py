import json
from itertools import chain, combinations
from urllib.parse import parse_qs
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor  # Используем ThreadPoolExecutor вместо ProcessPoolExecutor
from aiohttp import web

class SubsetSumHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)  # Изменяем на ThreadPoolExecutor

    async def get_subsets_handler(self, request):
        start_time = round(time.time() * 1000, 3)

        try:
            query_params = request.rel_url.query
            sum_value = int(query_params['sum'])
            query_data = json.loads(query_params['data'])
        except (ValueError, json.JSONDecodeError, KeyError):
            return web.Response(status=400, text='Bad Request: Invalid parameter values\n')

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self.executor, self.solve_subset_sum, query_data, sum_value)

        response_data = {'result': result}
        end_time = round(time.time() * 1000, 3)
        delta_time = round(end_time - start_time, 3)
        print(f'Request Processing Time: {delta_time}ms')

        return web.json_response(response_data)

    def solve_subset_sum(self, data, target_sum):
        all_subsets = list(chain.from_iterable(combinations(data, r) for r in range(len(data) + 1)))
        result_subsets = [list(subset) for subset in all_subsets if subset and sum(subset) == target_sum]
        length_result_subsets = len(result_subsets)
        print(length_result_subsets)
        return length_result_subsets

async def run_app():
    app = web.Application()
    handler = SubsetSumHandler()

    app.router.add_get('/getSubsets', handler.get_subsets_handler)
    app.router.add_route('*', '/{path:.*}', lambda r: web.Response(text="Successful!", status=200))

    server = await loop.create_server(app.make_handler(), '0.0.0.0', 8001)
    print('Started server on port 8001')

    return server

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(run_app())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
