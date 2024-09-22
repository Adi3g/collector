import logging
import os

def get_logger(name='collector', log_file='collector.log', level=logging.DEBUG):
    """
    Creates a logger instance for the Collector library.
    
    :param name: Name of the logger (usually the module name).
    :type name: str
    :param log_file: Path to the log file.
    :type log_file: str
    :param level: Logging level.
    :type level: int
    :return: Configured logger.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handlers
    c_handler = logging.StreamHandler()  # Console handler
    f_handler = logging.FileHandler(log_file)  # File handler

    # Set levels for handlers
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
