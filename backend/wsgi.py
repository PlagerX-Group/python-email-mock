import os

from flask import Flask

import configuration
from application import factory_create_application


def create_run_application() -> Flask:
    conf = configuration.get_configuration(os.getenv('ENVIRON', 'development'))
    conf.set_db_type(os.getenv('DATABASE_TYPE'))
    return factory_create_application(conf)


if __name__ == "__main__":
    flask_host, flask_port, environ = os.getenv('BACKEND_HOSTNAME', '0.0.0.0'), \
                                      os.getenv('BACKEND_PORT', '8087'), \
                                      os.getenv('ENVIRON', 'development')
    application = create_run_application()
    application.run(host=flask_host, port=flask_port)
