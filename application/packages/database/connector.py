import typing as t

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


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


class SMTPDatabaseConnector(Connector):

    def append_message(self):
        pass
