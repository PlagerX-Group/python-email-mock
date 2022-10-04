import enum

from flask_sqlalchemy import SQLAlchemy


class CommandHostDomainEnum(enum.Enum):
    HELO: int = 0
    EHLO: int = 1

    @staticmethod
    def to_enum(e: str):
        mapper = {'helo': CommandHostDomainEnum.HELO,
                  'ehlo': CommandHostDomainEnum.EHLO}
        return mapper.get(e)


class BaseORMModel(object):

    @property
    def as_json(self) -> dict:
        raise NotImplementedError()


# class UsersModel(db.Model, _BaseModel):
#     __tablename__ = "users"
#
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
#     username = db.Column(db.Text, unique=True)
#     password = db.Column(db.Text, unique=True)
#     show_name = db.Column(db.Text, unique=True)
#
#     def __str__(self) -> str:
#         return f"<{self.__class__.__name__} username='{self.username}'>"
#
#     def __repr__(self) -> str:
#         return f"<{self.__class__.__name__} username='{self.username}'>"
#
#     @property
#     def as_json(self) -> dict:
#         return {'id': self.id, 'username': self.username, 'show_name': self.show_name}


class BaseSMTPMessagesCommandsModel(BaseORMModel):
    __tablename__ = "smtp_messages_commands"
    __table_args__ = {'extend_existing': True}

    message_id = None
    message_uuid = None
    helo_or_ehlo = None
    mail_from = None
    mail_rcpt_tos = None
    mail_data = None

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.message_uuid}' mail_from='{self.mail_from}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.message_uuid}' mail_from='{self.mail_from}'>"

    @property
    def as_json(self) -> dict:
        return {'uuid': self.message_uuid,
                'mail_from': self.mail_from,
                'rcpt_to': self.mail_rcpt_tos,
                'helo': self.helo_or_ehlo == CommandHostDomainEnum.HELO,
                'ehlo': self.helo_or_ehlo == CommandHostDomainEnum.EHLO,
                'data': self.mail_data}


class BaseSMTPMessagesRawModel(BaseORMModel):
    __tablename__ = "smtp_messages_raw"
    __table_args__ = {'extend_existing': True}

    raw_id = None
    message_id = None
    raw_uuid = None
    content_type = None
    data = None
    mail_from = None
    mail_tos = None
    mail_message_id = None
    mime_version = None
    subject = None
    external_command = None

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} message_id='{self.message_id}' mail_from='{self.mail_from}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} message_id='{self.message_id}' mail_from='{self.mail_from}'>"

    @property
    def as_json(self) -> dict:
        return {'uuid': self.raw_uuid,
                'Content-Type': self.content_type,
                'Mime-Version': self.mime_version,
                'DATA': self.data,
                'MAIL FROM': self.mail_from,
                'MAIL TO': self.mail_tos,
                'Message-Id': self.message_id,
                'SUBJECT': self.subject}


class BaseSMTPMessagesAttachmentsModel(BaseORMModel):
    __tablename__ = "smtp_messages_attachments"
    __table_args__ = {'extend_existing': True}

    attachment_id = None
    raw_id = None
    attachment_uuid = None
    aws_object_uuid = None
    external_raw = None

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.attachment_uuid}' aws_uuid='{self.aws_object_uuid}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.attachment_uuid}' aws_uuid='{self.aws_object_uuid}'>"

    @property
    def as_json(self) -> dict:
        return {'uuid': self.attachment_uuid,
                'aws_object_id': self.aws_object_uuid}
