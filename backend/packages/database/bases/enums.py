import enum

from packages.database.pkg_postgres.connector import SMTPDatabasePostgresConnector
from packages.database.pkg_postgres.models import db as db_postgres
from packages.database.pkg_sqlite3.connector import SMTPDatabaseSqlite3Connector
from packages.database.pkg_sqlite3.models import db as db_sqlite3


@enum.unique
class SConnectorType(enum.Enum):
    POSTGRES = 0
    SQLITE3 = 1

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def get_connector_class(self):
        mapper = {SConnectorType.POSTGRES: SMTPDatabasePostgresConnector,
                  SConnectorType.SQLITE3: SMTPDatabaseSqlite3Connector}
        return mapper.get(self)

    def get_ext_db(self):
        mapper = {SConnectorType.POSTGRES: db_postgres,
                  SConnectorType.SQLITE3: db_sqlite3}
        return mapper.get(self)

    @staticmethod
    def to_enum(value: str):
        mapper = {'postgres': SConnectorType.POSTGRES,
                  'sqlite3': SConnectorType.SQLITE3}
        return mapper.get(value, SConnectorType.SQLITE3)

    @staticmethod
    def to_str_value(enums: enum.Enum) -> str:
        mapper = {SConnectorType.POSTGRES: '"postgres"',
                  SConnectorType.SQLITE3: '"sqlite3"'}
        return mapper.get(enums)

    @staticmethod
    def connector_types() -> str:
        return ", ".join([
            SConnectorType.to_str_value(SConnectorType.SQLITE3),
            SConnectorType.to_str_value(SConnectorType.POSTGRES)
        ])
