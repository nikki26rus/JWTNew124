"""Added the initial migration

Revision ID: e0d6bf9ab6c5
Revises: 99ff2be5acdb
Create Date: 2025-01-09 12:32:40.711305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0d6bf9ab6c5'
down_revision: Union[str, None] = '99ff2be5acdb'
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
