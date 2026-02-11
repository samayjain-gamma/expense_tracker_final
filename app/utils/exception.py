import sys
import traceback

from app.utils.logger import get_logger

logger = get_logger()


class CustomException(Exception):
    def __init__(self, error_message: str):
        super().__init__(error_message)
        self.error_message = error_message
        self.log_exception()

    def log_exception(self):
        exc_type, exc_value, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno

        logger.error(
            {
                "error": str(self.error_message),
                "file": file_name,
                "line": line_no,
                "trace": traceback.format_exc(),
            }
        )

    def __str__(self):
        return str(self.error_message)
