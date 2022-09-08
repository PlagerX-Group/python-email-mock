import os

from flask import Flask

import configuration
from application import factory_create_application


def create_run_application() -> Flask:
    _environ = os.getenv('ENVIRON', 'development')
    return factory_create_application(configuration.get_configuration(_environ))


if __name__ == "__main__":
    flask_host, flask_port, environ = os.getenv('BACKEND_HOSTNAME', '0.0.0.0'), \
                                      os.getenv('BACKEND_PORT', '8087'), \
                                      os.getenv('ENVIRON', 'development')
    application = factory_create_application(configuration.get_configuration(environ))
    application.run(host=flask_host, port=flask_port)
