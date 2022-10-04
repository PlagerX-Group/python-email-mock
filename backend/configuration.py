import os

from packages.database.bases.enums import SConnectorType


class BaseConfiguration(object):
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ECHO: bool = None
    SQLALCHEMY_ENGINE_OPTIONS = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = None
    IS_CREATE_TABLES: bool = None
    SQLITE_PATH: str = None

    def set_db_type(self, connector_type: SConnectorType):

        if connector_type == SConnectorType.POSTGRES:
            # TODO: добавить параметры окружения для подключения к POSTGRES.
            self.SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:password@0.0.0.0:6432/smtp_mock'
        elif connector_type == SConnectorType.SQLITE3:
            self.SQLALCHEMY_ENGINE_OPTIONS = {}
            if sqlite_path := os.getenv('SQLITE3_DB_PATH'):
                self.SQLITE_PATH = sqlite_path
            else:
                self.SQLITE_PATH = os.path.join(os.curdir, 'local-sqlite3.db')
            self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{self.SQLITE_PATH}"


class DevelopmentConfiguration(BaseConfiguration):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 2, 'connect_args': {'connect_timeout': 10}, 'pool_pre_ping': True}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    IS_CREATE_TABLES = True


class ProductionConfiguration(BaseConfiguration):
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 2, 'connect_args': {'connect_timeout': 10}, 'pool_pre_ping': True}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    IS_CREATE_TABLES: bool = False


def get_configuration(environ: str) -> BaseConfiguration:
    if environ == 'development':
        return DevelopmentConfiguration()
    elif environ == 'production':
        return ProductionConfiguration()
