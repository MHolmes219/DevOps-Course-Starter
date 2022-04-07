FROM python:3.8 as base

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

COPY ./todo_app /app/todo_app
COPY ./tests /app/tests
COPY poetry.lock pyproject.toml gunicorn_starter.sh /app

RUN pip3 install poetry

EXPOSE 5000

FROM base as development

RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as production

RUN poetry install --no-dev
ENTRYPOINT ["./gunicorn_starter.sh"]

FROM base as test

RUN poetry install
ENTRYPOINT ["poetry", "run", "pytest"]