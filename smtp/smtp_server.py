from aiosmtpd.smtp import SMTP as Server, syntax

from utils.logger import smtp_logger


class SMTPServer(Server):

    @syntax('SUBJECT: <subject> [ignored]')
    async def smtp_SUBJECT(self, arg: str):
        await self.push('259 Successfully update SUBJECT')
