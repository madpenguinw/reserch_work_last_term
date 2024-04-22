from http.server import HTTPServer

from server.logger import custom_logger
from server.logic import SubsetSumHandler


def run(
    server_class=HTTPServer,
    handler_class=SubsetSumHandler,
    port=8000,
    host="0.0.0.0",
):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    custom_logger.info(f"Started server on port {port}")
    httpd.serve_forever()
