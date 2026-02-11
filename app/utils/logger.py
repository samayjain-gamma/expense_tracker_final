import json
import logging
import os
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "filename": record.filename,
            "lineno": record.lineno,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


def get_logger(name: str = "app_logger"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    file_path = os.path.join(log_dir, file_name)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(file_path)
    formatter = JsonFormatter()
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


logger = get_logger()
