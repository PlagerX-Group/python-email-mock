import os

from smtp_controller import SMTPController
from smtp_handler import SMTPHandler

from utils.logger import smtp_logger


if __name__ == "__main__":
    controller = SMTPController(SMTPHandler(), hostname=os.getenv('SMTP_HOSTNAME'), port=os.getenv('SMTP_PORT'))

    try:
        smtp_logger.configure('Preparations for the launch of the SMTP')
        controller.start()
        smtp_logger.configure('Server successfully configured')
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        smtp_logger.configure('Preparing to shut down the server')
        controller.stop()
        smtp_logger.configure('Server stopped')
