import os

from flask import Flask

import configuration

from application import factory_create_application
from packages.database.bases.enums import SConnectorType
from packages.database.exceptions import ConnectorTypeNotAllowedException


def create_run_application() -> Flask:
    if connector_type := SConnectorType.to_enum(os.getenv('DATABASE_TYPE', '')):
        conf = configuration.get_configuration(os.getenv('ENVIRON', 'development'))
        conf.set_db_type(connector_type)
        return factory_create_application(conf, connector_type)
    raise ConnectorTypeNotAllowedException(f"Incorrect connector type: {connector_type}. "
                                           f"Expected: {SConnectorType.connector_types()}")


if __name__ == "__main__":
    flask_host, flask_port, environ = os.getenv('BACKEND_HOSTNAME', '0.0.0.0'), \
                                      os.getenv('BACKEND_PORT', '8087'), \
                                      os.getenv('ENVIRON', 'development')
    application = create_run_application()
    application.run(host=flask_host, port=flask_port)
