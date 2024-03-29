FROM python:3.8 as base

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

WORKDIR /app

RUN pip3 install poetry
COPY poetry.lock pyproject.toml /app/
RUN chmod a+x /app/pyproject.toml

EXPOSE 5001

RUN poetry config virtualenvs.create false --local && poetry install

COPY ./todo_app /app/todo_app

FROM base as development

ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0", "--port", "5001"]

FROM base as production

COPY gunicorn_starter.sh /app
RUN chmod +x /var/log

ENTRYPOINT ["./gunicorn_starter.sh"]

FROM base as test

COPY ./tests /app/tests
ENTRYPOINT ["poetry", "run", "pytest"]