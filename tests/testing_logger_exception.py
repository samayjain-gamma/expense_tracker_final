from app.utils.exception import CustomException
from app.utils.logger import logger


def test_logger_exception():
    logger.info("---going into the function testing_logger_exception---")
    try:
        1 / 0
    except Exception as e:
        logger.error("error occured")
        raise CustomException("something happened") from e


if __name__ == "__main__":
    test_logger_exception()
