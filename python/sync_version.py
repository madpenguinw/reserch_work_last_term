from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from itertools import chain, combinations
from urllib.parse import parse_qs
import time

class SubsetSumHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = self.path.split('?')
        path = parsed_url[0]
        
        # Используем time.time() для начала отсчета времени
        start_time = round(time.time() * 1000, 3)

        if path == '/getSubsets':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Получаем параметры запроса
            query_string = parsed_url[1]
            query_params = parse_qs(query_string)
            
            if 'data' not in query_params or 'sum' not in query_params:
                self.send_response(400, 'Bad Request: Missing required parameters\n')
                return

            try:
                sum_value = int(query_params['sum'][0])
                query_data = json.loads(query_params['data'][0])
            except (ValueError, json.JSONDecodeError):
                self.send_response(400, 'Bad Request: Invalid parameter values\n')
                return

            # Решаем задачу Subset Sum
            result = self.solve_subset_sum(query_data, sum_value)

            # Отправляем результат в формате JSON
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Successful!".encode())

        # Используем time.time() для окончания отсчета времени
        end_time = round(time.time() * 1000, 3)
        delta_time = round(end_time - start_time, 3)
        print(f'Request Processing Time: {delta_time}ms')

    def solve_subset_sum(self, data, target_sum):
        # Получаем все подмножества множества данных
        all_subsets = list(chain.from_iterable(combinations(data, r) for r in range(len(data) + 1)))

        # Фильтруем подмножества, сумма элементов которых равна target_sum
        result_subsets = [list(subset) for subset in all_subsets if subset and sum(subset) == target_sum]
        length_result_subsets = len(result_subsets)
        print(length_result_subsets)
        return length_result_subsets

def run(server_class=HTTPServer, handler_class=SubsetSumHandler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Started server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
