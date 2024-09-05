"""create users table

Revision ID: 6f95b56d7c8b
Revises: b4309d48b34d
Create Date: 2024-08-31 21:52:24.223826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f95b56d7c8b'
down_revision: Union[str, None] = 'b4309d48b34d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authentication",
        sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
         sa.Column("email",sa.String(),nullable=False,unique=True),
          sa.Column("password",sa.String(),nullable=False)
    )
    op.create_foreign_key('blogs_users',source_table="blogs",referent_table="authentication",
                          local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")




def downgrade() -> None:
    op.drop_table("authentication")
    op.drop_constraint('blogs_users')