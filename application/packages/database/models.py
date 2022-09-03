import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class _BaseModel(object):
    pass


class UsersModel(db.Model, _BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, unique=True)
    show_name = db.Column(db.Text, unique=True)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} username='{self.username}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} username='{self.username}'>"


class SMTPMessagesModel(db.Model, _BaseModel):
    __tablename__ = "smtp_messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    message_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())
    mail_date = db.Column(db.DateTime)
    mail_from = db.Column(db.Text)
    mail_rcpt_tos = db.Column(db.JSON, default=[])
    mail_subject = db.Column(db.Text, nullable=True)
    mail_source = db.Column(db.Text)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} " \
               f"uuid='{self.message_uuid}' date='{self.mail_date}' mail_from='{self.mail_from}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} " \
               f"uuid='{self.message_uuid}' date='{self.mail_date}' mail_from='{self.mail_from}'>"


class SMTPMessagesAttachmentsModel(db.Model, _BaseModel):
    __tablename__ = "smtp_messages_attachments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    message_id = db.Column(UUID(as_uuid=True), db.ForeignKey('smtp_messages.id'), unique=True, default=uuid.uuid4())
    attachment_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())
    aws_object_uuid = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4())

    external_message = db.relationship('SMTPMessagesModel', backref=db.backref('message', lazy=True))

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.attachment_uuid}' aws_uuid='{self.aws_object_uuid}'>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} uuid='{self.attachment_uuid}' aws_uuid='{self.aws_object_uuid}'>"
