from sqlalchemy.ext.declarative import declarative_base

SMTPDeclarativeBase = declarative_base()


class SMTPMessagesModel(SMTPDeclarativeBase):
    __tablename__ = "smtp_messages"
    uuid = None
    mail_date = None
    mail_from = None
    mail_subject = None
    mail_sender = None
    mail_reply_to = None
    source = None  # Исходное сообщение, пришедшее от отправителя


class SMTPMessagesAttachmentsModel(SMTPDeclarativeBase):
    __tablename__ = "smtp_messages_attachments"
