def setupLogging(log, handlers, sys):
    logging = log.getLogger('yolo')
    logging.propagate = False # so we don't get any conflicts with the abseil logger
    logging.setLevel(log.INFO)
    # logging is a singleton, make sure we don't duplicate the handlers and spawn additional log messages
    if not logging.handlers:
        logHandler = log.StreamHandler()
        logHandler.setLevel(log.INFO)
        logHandler.setFormatter(log.Formatter("%(asctime)s - %(levelname)s - %(message)s", '%m/%d/%Y %I:%M:%S %p'))
        logging.addHandler(logHandler)

    return logging