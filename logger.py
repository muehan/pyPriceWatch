import logging
import logging.handlers
import os

debugLogger = {}
errorLogger = {}

def info(message):
    if os.name != 'nt':
        logger = getDebugLogger()
        logger.info(message)
    else:
        print("info: " + message)


def error(message):
    if os.name != 'nt':
        logger = getErrorLogger()
        logger.info(message)
    else:
        print("error: " + message)

def getDebugLogger():
    global debugLogger
    if debugLogger:
        return debugLogger
    else:
        debugLogger = logging.getLogger('PriceWatchLogger')
        debugLogger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        debugLogger.addHandler(handler)
        return debugLogger

def getErrorLogger():
    global errorLogger
    if errorLogger:
        return errorLogger
    else:
        logger = logging.getLogger('PriceWatchLogger')
        logger.setLevel(logging.ERROR)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        logger.addHandler(handler)
        return errorLogger