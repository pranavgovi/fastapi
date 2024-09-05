"""add columns to post table

Revision ID: b4309d48b34d
Revises: 4a4d21fe2277
Create Date: 2024-08-31 21:39:51.149889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4309d48b34d'
down_revision: Union[str, None] = '4a4d21fe2277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.alter_column('blogs', 'id', new_column_name='blog_id')
    op.add_column(
        'blogs',sa.Column("user_id",sa.Integer(),nullable=False)
    )
    op.add_column(
        'blogs',sa.Column("time",sa.TIMESTAMP,nullable=False,server_default=sa.text("CURRENT_TIMESTAMP"))
    )
    op.add_column(
        'blogs',sa.Column("votes",sa.Integer(),nullable=False,default=0)
    )

    
    

def downgrade() -> None:
    
    op.alter_column('blogs', 'blog_id', new_column_name='id')
    op.drop_column('blogs','user_id')
    op.drop_column('blogs','time')
    op.drop_column('blogs','votes')
