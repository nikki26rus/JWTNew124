"""Added the initial migration

Revision ID: 7d9b2736baed
Revises: ad1877fe5674
Create Date: 2024-12-27 10:18:54.713170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d9b2736baed'
down_revision: Union[str, None] = 'ad1877fe5674'
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
