import logging
import logging.handlers
import os

def info(message):
    if os.name != 'nt':
        logger = logging.getLogger('PriceWatchLogger')
        logger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        logger.addHandler(handler)
        logger.info(message)
    else:
        print("info: " + message)


def error(message):
    if os.name != 'nt':
        logger = logging.getLogger('PriceWatchLogger')
        logger.setLevel(logging.ERROR)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        logger.addHandler(handler)
        logger.info(message)
    else:
        print("error: " + message)