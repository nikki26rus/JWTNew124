"""Added the initial migration

Revision ID: dc5d41b2b52f
Revises: fd2b41c25169
Create Date: 2024-12-20 16:16:12.629295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc5d41b2b52f'
down_revision: Union[str, None] = 'fd2b41c25169'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
