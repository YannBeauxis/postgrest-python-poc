FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
RUN apt-get update && apt-get install -y gcc libpq-dev
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-interaction --no-ansi -vvv --only main,migration --no-root

FROM python as runtime
RUN apt-get update && apt-get install -y libpq-dev
COPY --from=poetry /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY postgrest /app/postgrest
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini
# ENV PYTHONPATH="${PYTHONPATH}:/app/api"
CMD alembic upgrade head
