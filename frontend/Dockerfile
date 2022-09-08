FROM python:3.9.6-slim

MAINTAINER "Kirill Matveev / matveevkirill@internet.ru"

# Environment variables
ENV TZ "Europe/Moscow"
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYVER 3.9.6
ENV VIRTUAL_ENV /opt/venv
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
