ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# TODO: Enter this
ENV CLIENT_SECRET ENTER_YOUR_CLIENT_SECRET 

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
  pip install --upgrade pip && \
  pip install -r /tmp/requirements.txt && \
  rm -rf /root/.cache/

COPY . /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
RUN chmod +x ./start.sh
CMD ["./start.sh"]
