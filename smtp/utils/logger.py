import logging
import typing as t


class smtp_logger(object):
    __DEFAULT_LOGGER_NAME: str = 'smtp-server-logger'
    __LOGGER_FORMAT: str = r'[%(log_class)s] %(asctime)s %(message)s'

    @classmethod
    def __log(cls, message: str, extra: dict = None) -> t.NoReturn:
        if extra is None:
            extra = {'log_class': 'INFO'}

        logging.basicConfig(format=cls.__LOGGER_FORMAT)
        logger = logging.getLogger(cls.__DEFAULT_LOGGER_NAME)
        logger.setLevel(logging.INFO)
        logger.info(message, extra=extra)

    @classmethod
    def configure(cls, message: str) -> t.NoReturn:
        cls.__log(message, extra={'log_class': 'SMTP_CONFIGURE'})

    @classmethod
    def smtp_message(cls, mail_from: str, mail_to: str, content: str, is_auth: bool = False) -> t.NoReturn:
        end_string = '\n'
        message = f"MESSAGE_FROM_CLIENT:\n" \
                  f"======BEGIN=====\n" \
                  f"IS AUTH: {is_auth}\n" \
                  f"MAIL FROM: {mail_from}\n" \
                  f"MAIL TO: {mail_to}\n" \
                  f"----------CONTENT----------\n" \
                  f"{content}" \
                  f"{end_string if not content.endswith(end_string) else ''}=======END======="
        cls.__log(message, extra={'log_class': 'SMTP_MESSAGE'})
