from smtp_controller import SMTPController
from smtp_handler import SMTPHandler

from utils.logger import smtp_logger


if __name__ == "__main__":
    controller = SMTPController(SMTPHandler(), hostname='localhost', port=8025)

    try:
        smtp_logger.configure('Preparations for the launch of the SMTP')
        controller.start()
        smtp_logger.configure('Server successfully configured')
        input()
    except KeyboardInterrupt:
        pass
    finally:
        smtp_logger.configure('Preparing to shut down the server')
        controller.stop()
        smtp_logger.configure('Server stopped')
