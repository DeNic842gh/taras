"""add username to users

Revision ID: 20260521_0002
Revises: 20260519_0001
Create Date: 2026-05-21

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260521_0002"
down_revision: Union[str, Sequence[str], None] = "20260519_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=64), nullable=True))
    op.execute(
        "UPDATE users SET username = split_part(email, '@', 1) || '_' || id::text WHERE username IS NULL"
    )
    op.alter_column("users", "username", nullable=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_column("users", "username")
