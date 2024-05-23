"""alter_exception_column_in_members

Revision ID: 39b3e770f558
Revises: 
Create Date: 2024-05-23 21:14:56.591233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "39b3e770f558"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        table_name="members",
        column_name="exception",
        existing_type=sa.BOOLEAN(),
        type_=sa.String(length=10),
        nullable=True,
        server_default="No",
    )


def downgrade() -> None:
    pass
