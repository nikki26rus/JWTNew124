"""Added the initial migration

Revision ID: 802b94dbd41c
Revises: ada8b25fba9d
Create Date: 2024-12-23 07:17:24.707158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '802b94dbd41c'
down_revision: Union[str, None] = 'ada8b25fba9d'
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
