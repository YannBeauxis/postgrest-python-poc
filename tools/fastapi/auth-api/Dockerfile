FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
RUN apt-get update && apt-get install -y gcc
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-interaction --no-ansi -vvv --only main --no-root

FROM python as runtime
COPY --from=poetry /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY auth /app/api
ENV PYTHONPATH="${PYTHONPATH}:/app/api"
EXPOSE ${PORT}
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT}
