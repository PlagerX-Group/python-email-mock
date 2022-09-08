import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class CommandHostDomainEnum(enum.Enum):
    HELO: int = 0
    EHLO: int = 1

    @staticmethod
    def to_enum(e: str):
        mapper = {'helo': CommandHostDomainEnum.HELO,
                  'ehlo': CommandHostDomainEnum.EHLO}
        return mapper.get(e)


class _BaseModel(object):

    @property
    def as_json(self) -> dict:
        raise NotImplementedError()


class UsersModel(db.Model, _BaseModel):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=True)
    show_name = db.Column(db.Text, unique=True)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} username='{self.username}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} username='{self.username}'>"

    @property
    def as_json(self) -> dict:
        return {'id': self.id, 'username': self.username, 'show_name': self.show_name}


class SMTPMessagesCommandsModel(db.Model, _BaseModel):
    __tablename__ = "smtp_messages_commands"

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    message_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())
    helo_or_ehlo = db.Column(db.Enum(CommandHostDomainEnum, name='helo_or_ehlo'), default=CommandHostDomainEnum.HELO)
    mail_from = db.Column(db.Text)
    mail_rcpt_tos = db.Column(db.JSON, default=[])
    mail_data = db.Column(db.Text, nullable=True)

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


class SMTPMessagesRawModel(db.Model, _BaseModel):
    __tablename__ = "smtp_messages_raw"

    raw_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    message_id = db.Column(db.Integer, db.ForeignKey('smtp_messages_commands.message_id'),
                           unique=True, default=uuid.uuid4())
    raw_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())
    content_type = db.Column(db.Text, nullable=True)
    data = db.Column(db.Text, nullable=True)
    mail_from = db.Column(db.Text)
    mail_tos = db.Column(db.JSON, default=[])
    mail_message_id = db.Column(db.Text, default=None)
    mime_version = db.Column(db.Text, nullable=True)
    subject = db.Column(db.Text, nullable=True)

    external_command = db.relationship('SMTPMessagesCommandsModel', backref=db.backref('command', lazy=True))

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


class SMTPMessagesAttachmentsModel(db.Model, _BaseModel):
    __tablename__ = "smtp_messages_attachments"

    attachment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    raw_id = db.Column(db.Integer, db.ForeignKey('smtp_messages_raw.raw_id'), unique=True, default=uuid.uuid4())
    attachment_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())
    aws_object_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())

    external_raw = db.relationship('SMTPMessagesRawModel', backref=db.backref('raw', lazy=True))

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.attachment_uuid}' aws_uuid='{self.aws_object_uuid}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.attachment_uuid}' aws_uuid='{self.aws_object_uuid}'>"

    @property
    def as_json(self) -> dict:
        return {'uuid': self.attachment_uuid,
                'aws_object_id': self.aws_object_uuid}
