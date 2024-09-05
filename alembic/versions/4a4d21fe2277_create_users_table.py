"""Update posts table

Revision ID: 4a4d21fe2277
Revises: c3f46904a149
Create Date: 2024-08-31 20:49:24.031508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a4d21fe2277'
down_revision: Union[str, None] = 'c3f46904a149'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("posts","blogs")
    
    
    

def downgrade() -> None:
    op.rename_table("blogs","posts")
    
