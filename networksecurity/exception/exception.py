import sys
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: tuple):
        super().__init__(error_message)
        _, _, exc_tb = error_details or (None, None, None)

        self.lineno = exc_tb.tb_lineno if exc_tb else "Unknown"
        self.file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
        self.error_message = error_message

    def __str__(self):
        return (
            f"Error occurred in python script name [{self.file_name}] "
            f"line number [{self.lineno}] error message [{self.error_message}]"
        )

if __name__ == '__main__':
    try:
        logger.info("Entering the try block")
        a = 1 / 0
        print("This will not be printed", a)
    except Exception as e:
        custom_exception = NetworkSecurityException(e, sys.exc_info())
        logger.error(custom_exception)
        raise custom_exception
