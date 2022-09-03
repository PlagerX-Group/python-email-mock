import logging
import typing as t

from flask import Flask, g

from packages.database import ext_db, SMTPDatabaseConnector
from packages.router import index_blueprint, smtp_blueprint


def register_blueprints(flask_app: Flask) -> t.NoReturn:
    flask_app.register_blueprint(index_blueprint)
    flask_app.register_blueprint(smtp_blueprint)


def register_extensions(flask_app: Flask) -> t.NoReturn:
    ext_db.init_app(flask_app)


def register_application_configuration(flask_app: Flask, flask_configuration) -> t.NoReturn:

    # Engine for database
    engine = ext_db.create_engine(flask_configuration.SQLALCHEMY_DATABASE_URI,
                                  flask_configuration.SQLALCHEMY_ENGINE_OPTIONS)

    # Connector database
    connector = SMTPDatabaseConnector(engine=engine)

    @flask_app.before_request
    def start_session():
        connector.create_connection()
        g.connector = connector

    @flask_app.teardown_request
    def shutdown_session(exception):
        _connector = g.pop('connector')
        if exception is None:
            _connector.commit()
            _connector.close_connection()
        else:
            _connector.flush()
            _connector.close_connection()


def factory_create_application(flask_configuration) -> Flask:
    flask_app = Flask(__name__)

    flask_app.config.from_object(flask_configuration)

    register_blueprints(flask_app)
    register_extensions(flask_app)
    register_application_configuration(flask_app, flask_configuration)

    # Logger
    gunicorn_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)

    return flask_app
