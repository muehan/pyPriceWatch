import logging
import logging.handlers
import os

def info(message):
    if os.name != 'nt':
        logger = logging.getLogger('PriceWatchLogger')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        logger.addHandler(handler)
        logger.info(message)

def error(message):
    if os.name != 'nt':
        logger = logging.getLogger('PriceWatchLogger')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        logger.addHandler(handler)
        logger.info(message)