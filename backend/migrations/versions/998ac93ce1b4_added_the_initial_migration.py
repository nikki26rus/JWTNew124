"""Added the initial migration

Revision ID: 998ac93ce1b4
Revises: 8eab4e366c20
Create Date: 2025-01-06 18:13:55.209138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '998ac93ce1b4'
down_revision: Union[str, None] = '8eab4e366c20'
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
