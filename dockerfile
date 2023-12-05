FROM python:3.11.3-alpine3.18

ENV PYTHONDOWNTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY dolar_project /dolar_project

COPY scripts /scripts

COPY dotenv_files/.env /dolar_project/.env

WORKDIR /dolar_project

EXPOSE 8000

RUN apk add --no-cache build-base python3-dev && \
  python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /dolar_project/requirements.txt && \
  adduser --disabled-password --no-create-home dolar_project_admin && \
  mkdir -p /data && \
  chown -R dolar_project_admin:dolar_project_admin /venv && \
  chown -R dolar_project_admin:dolar_project_admin /data && \
  chmod -R 755 /data && \
  chmod -R +x /scripts


ENV PATH="/scripts:/venv/bin:$PATH"

USER dolar_project_admin

CMD ["commands.sh"]