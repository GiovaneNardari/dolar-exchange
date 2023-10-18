FROM python:3.11.3-alpine3.18

ENV PYTHONDOWNTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY dolar_project /dolar_project

COPY scripts /scripts

WORKDIR /dolar_project

EXPOSE 8000

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /dolar_project/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data && \
  chmod -R 755 /data && \
  chmod -R +x /scripts


ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["commands.sh"]