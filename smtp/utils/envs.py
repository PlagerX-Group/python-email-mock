import os


def validate_envs(environ_variables):
    variables = list(environ_variables)
    required_variables = ["SMTP_HOSTNAME", "SMTP_PORT", "BACKEND_HOSTNAME", "BACKEND_PORT"]

    for variable in required_variables:
        if not (variable in variables and os.environ.get(variable, default="") != ""):
            raise EnvironmentError(
                f"Required environment not set: {variable}"
            )


def set_default_environs():
    required_variables = {
        'SMTP_HOSTNAME': '0.0.0.0',
        'BACKEND_HOSTNAME': '0.0.0.0',
        'BACKEND_PORT': "0"
    }

    for k, v in required_variables.items():
        if not os.getenv(k):
            os.environ[k] = v
