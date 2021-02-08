import logging


def app_logger(name):
    base_logger = logging.getLogger(name)
    logging.basicConfig(
        format='%(asctime)s - %(name)s:%(message)s',
        filename='app.log',
        level=logging.INFO,
    )
    return base_logger
