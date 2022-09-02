from aiosmtpd.smtp import Envelope, Session, SMTP

from utils.logger import smtp_logger


class SMTPHandler(object):

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope):
        smtp_logger.smtp_message(mail_from=envelope.mail_from, mail_to=envelope.rcpt_tos, is_auth=session.authenticated,
                                 content=envelope.content.decode('utf8'))
        return '250 Message accepted for delivery'
