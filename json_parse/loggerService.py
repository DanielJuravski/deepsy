import logging

LOG_LEVEL = 20  # INFO
LOG_FILE = 'json_scripts.log'

def initLogger():
    logging.basicConfig(level=LOG_LEVEL)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] %(filename)s [%(levelname)s]  %(message)s")
    rootLogger = logging.getLogger()

    #fileHandler = logging.FileHandler(LOG_FILE)
    #fileHandler.setFormatter(logFormatter)
    #rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
