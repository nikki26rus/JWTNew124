"""Added the initial migration

Revision ID: 358f452004dc
Revises: e0d6bf9ab6c5
Create Date: 2025-01-09 12:39:59.449190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '358f452004dc'
down_revision: Union[str, None] = 'e0d6bf9ab6c5'
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