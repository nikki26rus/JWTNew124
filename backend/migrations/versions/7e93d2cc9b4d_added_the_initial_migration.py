"""Added the initial migration

Revision ID: 7e93d2cc9b4d
Revises: f9669cb9853a
Create Date: 2024-12-23 10:45:07.845093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e93d2cc9b4d'
down_revision: Union[str, None] = 'f9669cb9853a'
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