import os

from smtp_controller import SMTPController
from smtp_handler import SMTPHandler

from utils.logger import smtp_logger
from utils.envs import validate_envs, set_default_environs


if __name__ == "__main__":

    # Set default to environ
    set_default_environs()

    # Validate environ variables
    validate_envs(os.environ)

    # Configure SMTP-controller
    controller = SMTPController(SMTPHandler(), hostname=os.getenv('SMTP_HOSTNAME'), port=os.getenv('SMTP_PORT'))

    try:
        smtp_logger.configure('Preparations for the launch of the SMTP')
        controller.start()
        smtp_logger.configure('Server successfully configured')
        while True:
            pass
    except KeyboardInterrupt:
        exit(0)
    finally:
        smtp_logger.configure('Preparing to shut down the server')
        controller.stop()
        smtp_logger.configure('Server stopped')
