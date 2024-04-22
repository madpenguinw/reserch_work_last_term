import logging

custom_logger = logging.getLogger("custom_logger")
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s " "%(funcName)s: %(message)s"
)
stream_handler.setFormatter(formatter)
custom_logger.addHandler(stream_handler)
custom_logger.setLevel(logging.DEBUG)
