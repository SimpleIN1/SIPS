FROM python:3.9.0-slim AS builder
LABEL authors="SimpleIN1 <serbinovichgs@ict.nsc.ru>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG SERVICE_PATH=AccountingService

RUN useradd -s /bin/bash django-user \
     && mkdir -p /usr/src/app/AccountProject/ \
     && chown -R django-user:django-user /usr/src/app/

WORKDIR /usr/src/app/

USER django-user

COPY --chown=django-user:django-user ./backend/${SERVICE_PATH}/requirements.txt .

RUN python -m venv venv && venv/bin/python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    venv/bin/pip install -r requirements.txt

COPY --chown=django-user:django-user backend/${SERVICE_PATH}/AccountProject/ AccountProject
RUN chown -R django-user:django-user /usr/src/app/AccountProject/

WORKDIR /usr/src/app/AccountProject

FROM builder AS server-auth

ARG SERVICE_PATH=AuthenticationService

COPY --chown=django-user:django-user ./backend/AuthenticationService/start.sh ../
RUN chmod u+x /usr/src/app/start.sh

FROM builder AS server-account

ARG SERVICE_PATH=AccountingService

COPY --chown=django-user:django-user ./backend/AccountingService/entrypoint.sh  \
                                     ./backend/AccountingService/start.sh ../
RUN chmod u+x /usr/src/app/entrypoint.sh /usr/src/app/start.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

FROM builder AS celery

FROM python:3.9.0-slim AS server-info-composite
LABEL authors="SimpleIN1 <serbinovichgs@ict.nsc.ru>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -s /bin/bash django-user \
     && mkdir -p /usr/src/app/api/ \
     && chown -R django-user:django-user /usr/src/app/

WORKDIR /usr/src/app/

USER django-user

COPY --chown=django-user:django-user ./backend/InfoCompositeOutputDataRESTAPIService/requirements.txt .

RUN python -m venv venv && venv/bin/python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    venv/bin/pip install -r requirements.txt

COPY --chown=django-user:django-user ./backend/InfoCompositeOutputDataRESTAPIService/api/ api
COPY --chown=django-user:django-user ./backend/InfoCompositeOutputDataRESTAPIService/migrations migrations
COPY --chown=django-user:django-user ./backend/InfoCompositeOutputDataRESTAPIService/alembic.ini .
COPY --chown=django-user:django-user ./backend/InfoCompositeOutputDataRESTAPIService/start.sh .
RUN chmod u+x /usr/src/app/start.sh

RUN chown -R django-user:django-user /usr/src/app/

FROM python:3.9.0-slim AS server-docs-agregator
LABEL authors="SimpleIN1 <serbinovichgs@ict.nsc.ru>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -s /bin/bash django-user \
     && mkdir -p /usr/src/app/api/ \
     && chown -R django-user:django-user /usr/src/app/

WORKDIR /usr/src/app/

USER django-user

COPY --chown=django-user:django-user ./backend/DocsAgregatorSwaggerUI/requirements.txt .

RUN python -m venv venv && venv/bin/python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    venv/bin/pip install -r requirements.txt

COPY --chown=django-user:django-user ./backend/DocsAgregatorSwaggerUI/api/ api
COPY --chown=django-user:django-user ./backend/DocsAgregatorSwaggerUI/start.sh .
RUN chmod u+x /usr/src/app/start.sh

RUN chown -R django-user:django-user /usr/src/app/
