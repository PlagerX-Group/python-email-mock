import uuid

from flask_sqlalchemy import SQLAlchemy

from packages.database.bases.base_model import (
    BaseSMTPMessagesCommandsModel,
    BaseSMTPMessagesRawModel,
    BaseSMTPMessagesAttachmentsModel,
    CommandHostDomainEnum
)


db = SQLAlchemy()


class SMTPMessagesCommandsModel(BaseSMTPMessagesCommandsModel, db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    message_uuid = db.Column(db.Text(length=36), unique=True, default=lambda: str(uuid.uuid4()))
    helo_or_ehlo = db.Column(db.Enum(CommandHostDomainEnum, name='helo_or_ehlo'), default=CommandHostDomainEnum.HELO)
    mail_from = db.Column(db.Text)
    mail_rcpt_tos = db.Column(db.JSON, default=[])
    mail_data = db.Column(db.Text, nullable=True)


class SMTPMessagesRawModel(BaseSMTPMessagesRawModel, db.Model):
    raw_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    message_id = db.Column(db.Integer, db.ForeignKey('smtp_messages_commands.message_id'),
                           unique=True, default=uuid.uuid4())
    raw_uuid = db.Column(db.Text(length=36), unique=True, default=lambda: str(uuid.uuid4()))
    content_type = db.Column(db.Text, nullable=True)
    data = db.Column(db.Text, nullable=True)
    mail_from = db.Column(db.Text, nullable=True)
    mail_tos = db.Column(db.JSON, nullable=True, default=[])
    mail_message_id = db.Column(db.Text, nullable=True, default=None)
    mime_version = db.Column(db.Text, nullable=True)
    subject = db.Column(db.Text, nullable=True)
    external_command = db.relationship('SMTPMessagesCommandsModel', backref=db.backref('command', lazy=True))


class SMTPMessagesAttachmentsModel(BaseSMTPMessagesAttachmentsModel, db.Model):
    attachment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    raw_id = db.Column(db.Integer, db.ForeignKey('smtp_messages_raw.raw_id'), unique=True, default=uuid.uuid4())
    attachment_uuid = db.Column(db.Text(length=36), unique=True, default=lambda: str(uuid.uuid4()))
    aws_object_uuid = db.Column(db.Text(length=36), unique=True, default=lambda: str(uuid.uuid4()))
    external_raw = db.relationship('SMTPMessagesRawModel', backref=db.backref('raw', lazy=True))
