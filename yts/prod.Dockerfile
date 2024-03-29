###########
# BUILDER #
###########

FROM python:3.10.8-slim-buster as builder

RUN apt-get update \
  && apt-get -y install gcc postgresql \
  && apt-get clean

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
  && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . /usr/src/app/

RUN pip install black==21.12b0 flake8==4.0.1 isort==5.10.1

RUN flake8 .
RUN black --exclude=migrations .
RUN isort .

#########
# FINAL #
#########

FROM python:3.10.8-slim-buster

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
# RUN pip install --upgrade pip
# RUN pip install --no-cache /wheels/*
# RUN pip install "uvicorn[standard]==0.16.0"

COPY . .

RUN chown -R app:app $HOME

USER app

CMD gunicorn --bind 0.0.0.0:$PORT app.main:app -k uvicorn.workers.UvicornWorker
