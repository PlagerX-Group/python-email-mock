class BaseConfiguration(object):
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ECHO: bool = None
    SQLALCHEMY_ENGINE_OPTIONS = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = None
    RECREATE_DATABASE: bool = None


class DevelopmentConfiguration(BaseConfiguration):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@0.0.0.0:6432/postgres'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 2, 'connect_args': {'connect_timeout': 10}, 'pool_pre_ping': True}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RECREATE_DATABASE = True


class ProductionConfiguration(BaseConfiguration):
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 2, 'connect_args': {'connect_timeout': 10}, 'pool_pre_ping': True}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RECREATE_DATABASE: bool = False


def get_configuration(environ: str) -> BaseConfiguration:
    if environ == 'development':
        return DevelopmentConfiguration()
    elif environ == 'production':
        return ProductionConfiguration()
