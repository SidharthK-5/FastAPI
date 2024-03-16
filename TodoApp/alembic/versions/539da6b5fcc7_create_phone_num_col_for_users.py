"""Create phone num col for users

Revision ID: 539da6b5fcc7
Revises: 
Create Date: 2024-03-16 13:49:00.713661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "539da6b5fcc7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        table_name="users", column=sa.Column("phone_number", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column(table_name="users", column_name="phone_number")
