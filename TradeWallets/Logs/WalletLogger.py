import logging

def create_new_logger():
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    f_handler = logging.FileHandler('MainLog.log')
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)
    return logger