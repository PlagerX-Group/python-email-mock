FROM python:3.9.6-slim

MAINTAINER "Kirill Matveev / matveevkirill@internet.ru"

# Environment variables
ENV TZ "Europe/Moscow"
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYVER 3.9.6
ENV VIRTUAL_ENV /opt/venv
ENV ROOT_DIR "/python-smtp-mock"
ENV PATH "$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH "$PYTHONPATH:$ROOT_DIR/application"
ENV BACKEND_HOSTNAME "$BACKEND_HOSTNAME"
ENV BACKEND_PORT $BACKEND_PORT

WORKDIR $ROOT_DIR

# Copying require files and dirs
COPY requirements.txt requirements.txt
COPY . .

# Install requirements for python
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "-m", "gunicorn", \
     "wsgi:create_run_application()", \
     "--workers", "1", \
     "--bind", "0.0.0.0:9002"]