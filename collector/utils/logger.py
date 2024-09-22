import logging
import colorlog

def get_logger(name='Collector', log_file='collector.log', level=logging.DEBUG):
    """
    Creates a logger instance for the Collector library with colored log levels for console output.

    :param name: Name of the logger.
    :param log_file: Path to the log file.
    :param level: Logging level.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler with color
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)

    # File handler without color
    f_handler = logging.FileHandler(log_file)
    f_handler.setLevel(logging.DEBUG)

    # Color formatter for console (color only applied to log level)
    c_format = colorlog.ColoredFormatter(
        "%(name)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",  # Apply color only to log level
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
        reset=True
    )

    # Standard formatter for file logs
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatters to handlers
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
