import typing as t
import sqlalchemy
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from packages.database.bases.base_model import BaseSMTPMessagesCommandsModel, BaseSMTPMessagesRawModel
from packages.pymodels.smtp_models import PySMTPMessageModel


class BaseORMConnector:
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


class BaseORMConnectorMethods(BaseORMConnector):

    def get_command_by_uuid(
            self,
            command_uuid: uuid.UUID
    ) -> BaseSMTPMessagesCommandsModel:
        raise NotImplementedError

    def get_message_by_uuid(
            self,
            raw_uuid: uuid.UUID
    ) -> BaseSMTPMessagesRawModel:
        raise NotImplementedError

    def append_command(
            self,
            message: PySMTPMessageModel
    ) -> BaseSMTPMessagesCommandsModel:
        raise NotImplementedError

    def append_raw_message(
            self,
            command_mode: BaseSMTPMessagesCommandsModel,
            message: PySMTPMessageModel
    ) -> BaseSMTPMessagesRawModel:
        raise NotImplementedError
