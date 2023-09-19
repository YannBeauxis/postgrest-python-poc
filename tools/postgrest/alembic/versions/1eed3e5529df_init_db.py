"""Init DB

Revision ID: 1eed3e5529df
Revises: 
Create Date: 2023-05-25 13:56:51.166274

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "1eed3e5529df"
down_revision = None
branch_labels = None
depends_on = None

ANON_ROLE = "web_anon"
EDITOR_ROLE = "editor"
ROLES = [ANON_ROLE, EDITOR_ROLE]
SCHEMA = "api"


def upgrade() -> None:
    for role in ROLES:
        op.execute(f"create role {role} nologin INHERIT;")
        op.execute(f"grant {role} to admin;")

    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")

    for role in ROLES:
        op.execute(f"grant usage on schema {SCHEMA} to {role};")
        op.execute(
            (
                f"ALTER DEFAULT PRIVILEGES "
                f"IN SCHEMA {SCHEMA} GRANT USAGE "
                f"ON SEQUENCES to {role};"
            )
        )
        op.execute(
            f"GRANT SELECT, UPDATE, USAGE ON ALL SEQUENCES IN SCHEMA {SCHEMA} to {role}"
        )

    op.execute(
        (
            f"ALTER DEFAULT PRIVILEGES "
            f"IN SCHEMA {SCHEMA} GRANT SELECT ON TABLES TO {ANON_ROLE};"
        )
    )
    op.execute(
        (
            f"ALTER DEFAULT PRIVILEGES "
            f"IN SCHEMA {SCHEMA} GRANT ALL ON TABLES TO {EDITOR_ROLE};"
        )
    )


def downgrade() -> None:
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE;")

    for role in ROLES:
        op.execute(f"drop role {role};")
