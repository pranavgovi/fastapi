"""create votes table

Revision ID: 936dcc753d97
Revises: 6f95b56d7c8b
Create Date: 2024-08-31 21:59:18.099665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '936dcc753d97'
down_revision: Union[str, None] = '6f95b56d7c8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_primary_key('primarykey_blogs', 'blogs', ['blog_id'])
    op.create_table(
        "votes",
        sa.Column("post_id",sa.Integer(),sa.ForeignKey('blogs.blog_id',ondelete='CASCADE'),primary_key=True,nullable=False),
        sa.Column("user_id",sa.Integer(),sa.ForeignKey('authentication.id',ondelete='CASCADE'),primary_key=True,nullable=False)
    )


def downgrade() -> None:
    op.drop_constraint("primarykey_blogs")
    op.drop_table("votes")
