from aiosmtpd.smtp import Envelope, Session, SMTP

from rest.controller import APIController
from utils.logger import smtp_logger


class SMTPHandler(object):

    api_controller: APIController = None

    def __init__(self):
        self.api_controller = APIController()

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope):
        smtp_logger.smtp_message(mail_from=envelope.mail_from, mail_to=envelope.rcpt_tos, is_auth=session.authenticated,
                                 content=envelope.content.decode('utf8'))
        self.api_controller.send_message(mail_from=envelope.mail_from,
                                         mail_to=envelope.rcpt_tos,
                                         content=envelope.content.decode('utf-8'),
                                         helo_or_ehlo='helo'.lower())  # TODO: hardcode
        return '250 Message accepted for delivery'
