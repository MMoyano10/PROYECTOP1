import logging
import logging.handlers
import json
from pythonjsonlogger import jsonlogger
import os
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"

def setup_logging(service_name: str):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Cambiar a DEBUG para mostrar todos los niveles

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    log_format = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(service)s %(funcName)s'
    )

    # Console handler con color
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    color_formatter = ColorFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)

    # File handler
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, f'{service_name}.log'), maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Add service name to all logs
    logging.LoggerAdapter(logger, {'service': service_name})

    return logger 