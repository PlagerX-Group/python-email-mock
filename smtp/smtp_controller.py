from aiosmtpd.controller import Controller

from smtp_server import SMTPServer


class SMTPController(Controller):

    def factory(self):
        return SMTPServer(self.handler)
