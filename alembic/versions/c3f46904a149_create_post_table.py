"""Create post table

Revision ID: c3f46904a149
Revises: 
Create Date: 2024-08-31 20:36:57.818182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3f46904a149'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
         sa.Column("title",sa.String(),nullable=False),
          sa.Column("content",sa.String(),nullable=False),
          sa.Column("public",sa.Boolean(),nullable=False)
    )


def downgrade() -> None:
    op.drop_table("posts")
