import typing as t
import uuid
from email.parser import Parser

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from utils.functions import decode_quoted_printable_string, parse_multipart_in_email
from .models import SMTPMessagesCommandsModel, CommandHostDomainEnum, SMTPMessagesRawModel
from packages.pymodels.smtp_models import PySMTPMessageModel


class Connector:
    engine: Engine = None
    session: Session = None

    def __init__(self, engine: Engine) -> t.NoReturn:
        self.engine = engine

    def __del__(self) -> t.NoReturn:
        self.close_connection()

    @property
    def is_connected(self) -> bool:
        return self.session is not None

    def create_connection(self) -> t.NoReturn:
        self.session = Session(self.engine, expire_on_commit=False)

    def close_connection(self) -> t.NoReturn:
        if self.is_connected:
            self.session.close()

    def commit(self) -> t.NoReturn:
        if self.is_connected:
            self.session.commit()

    def flush(self) -> t.NoReturn:
        if self.is_connected:
            self.session.flush()

    def create_tables(self, base: SQLAlchemy) -> t.NoReturn:
        for table in list(base.metadata.tables.keys()):
            if not sqlalchemy.inspect(self.engine).has_table(table):
                base.metadata.tables[table].create(self.engine)


class SMTPDatabaseConnector(Connector):

    def get_command_by_uuid(self, command_uuid: uuid.UUID) -> SMTPMessagesCommandsModel:
        return self.session.query(SMTPMessagesCommandsModel). \
            filter(SMTPMessagesCommandsModel.message_uuid == command_uuid). \
            one_or_none()

    def get_message_by_uuid(self, raw_uuid: uuid.UUID) -> SMTPMessagesRawModel:
        return self.session.query(SMTPMessagesRawModel).\
            filter(SMTPMessagesRawModel.raw_uuid == raw_uuid).\
            one_or_none()

    def append_command(self, message: PySMTPMessageModel) -> SMTPMessagesCommandsModel:
        model = SMTPMessagesCommandsModel(message_uuid=uuid.uuid4(),
                                          mail_from=message.mail_from,
                                          helo_or_ehlo=CommandHostDomainEnum.to_enum(message.helo_or_ehlo),
                                          mail_rcpt_tos=message.mail_to,
                                          mail_data=message.mail_data)
        self.session.add(model)
        return model

    def append_raw_message(self,
                           command_mode: SMTPMessagesCommandsModel,
                           message: PySMTPMessageModel) -> SMTPMessagesRawModel:
        raw_data = message.mail_data
        headers = Parser().parsestr(raw_data)
        content_type = headers. \
            get('Content-Type', ''). \
            replace('\n', ''). \
            replace('\t', ''). \
            replace('\r', ''). \
            replace('\"', "\'") or None
        mail_from = decode_quoted_printable_string(headers.get('From', '').replace('\n', '').replace('\t', '') or None)

        model = SMTPMessagesRawModel(raw_uuid=uuid.uuid4(),
                                     content_type=content_type,
                                     data=parse_multipart_in_email(raw_data),
                                     mail_from=mail_from,
                                     mail_tos=list(headers.get('To')),
                                     mail_message_id=headers.get('Message-ID', '').lstrip('<').rstrip('>'),
                                     mime_version=headers.get('MIME-Version'),
                                     subject=decode_quoted_printable_string(headers.get('Subject')),
                                     external_command=command_mode)
        self.session.add(model)
        return model
