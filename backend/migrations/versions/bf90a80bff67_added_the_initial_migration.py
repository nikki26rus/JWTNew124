"""Added the initial migration

Revision ID: bf90a80bff67
Revises: c7551e4d1ee1
Create Date: 2024-12-21 00:56:23.581292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf90a80bff67'
down_revision: Union[str, None] = 'c7551e4d1ee1'
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
