from time import sleep
from typing import Generator

import pytest
from pytest import MonkeyPatch
import sqlalchemy
from sqlalchemy.engine import Engine
from python_on_whales import docker, DockerClient  # type: ignore
from pytest_alembic.runner import MigrationContext

from herbaltea_classifier.adapters.postgrest import (
    HmpcCrud,
    settings,
    PostgrestResource,
)

DB_ADMIN = "admin"
DB_PASSWORD = "pass"
DB_NAME = "db"
DB_PORT = 5432
SQL_ALCHEMY_URL = f"postgresql://{DB_ADMIN}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
PGRST_SECRET = "PGRST_JWT_SECRET_PGRST_JWT_SECRET_PGRST_JWT_SECRET_PGRST_JWT_SECRET"
ROLE_ANON = "web_anon"

PostgrestResource.get = PostgrestResource.read
PostgrestResource.post = PostgrestResource.create
PostgrestResource.patch = PostgrestResource.update


def wait_for_db() -> None:
    sleep(2)


@pytest.fixture(autouse=True)
def set_env(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("SQL_ALCHEMY_URL", SQL_ALCHEMY_URL)


@pytest.fixture(scope="session")
def db() -> Generator[DockerClient, None, None]:
    with docker.run(  # type: ignore
        "postgres",
        detach=True,
        remove=True,
        envs={
            "POSTGRES_USER": DB_ADMIN,
            "POSTGRES_PASSWORD": DB_PASSWORD,
            "POSTGRES_DB": DB_NAME,
        },
        networks=["host"],
        publish=[(DB_PORT, 5432)],
    ) as container:
        wait_for_db()
        yield container


@pytest.fixture(scope="session")
def alembic_engine(db: DockerClient) -> Engine:
    return sqlalchemy.create_engine(SQL_ALCHEMY_URL)


@pytest.fixture(scope="session")
def postgrest_(alembic_engine: Engine) -> Generator[DockerClient, None, None]:
    with docker.run(  # type: ignore
        "postgrest/postgrest",
        detach=True,
        remove=True,
        envs={
            "PGRST_DB_URI": SQL_ALCHEMY_URL,
            "PGRST_DB_SCHEMAS": "api",
            "PGRST_DB_ANON_ROLE": ROLE_ANON,
            "PGRST_JWT_SECRET": PGRST_SECRET,
            # "PGRST_LOG_LEVEL": "info",
        },
        networks=["host"],
        publish=[(3000, 3000)],
    ) as container:
        yield container


@pytest.fixture
def postgrest(
    postgrest_: DockerClient, alembic_runner: MigrationContext, alembic_engine: Engine
) -> Generator[DockerClient, None, None]:
    alembic_runner.migrate_up_to("head")
    postgrest_.kill("SIGUSR1")
    sleep(1)
    yield postgrest_
    alembic_runner.migrate_down_to("base")


@pytest.fixture
def client_anon(postgrest: DockerClient) -> HmpcCrud:
    return HmpcCrud("http://localhost:3000")


@pytest.fixture
def client_editor(postgrest: DockerClient, monkeypatch: MonkeyPatch) -> HmpcCrud:
    monkeypatch.setattr(settings, "secret_key", PGRST_SECRET)
    return HmpcCrud("http://localhost:3000")
