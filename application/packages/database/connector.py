import typing as t

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .models import SMTPMessagesModel
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

    def append_message(self, message: PySMTPMessageModel) -> SMTPMessagesModel:
        model = SMTPMessagesModel(mail_date='',
                                  mail_from=message.mail_from,
                                  mail_rcpt_tos=message.mail_to,
                                  # mail_subject=message.subject,
                                  mail_source=None)
        self.session.add(model)
        return model
