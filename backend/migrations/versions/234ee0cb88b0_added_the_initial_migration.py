"""Added the initial migration

Revision ID: 234ee0cb88b0
Revises: 5a93f307f84e
Create Date: 2024-12-20 16:00:27.170059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '234ee0cb88b0'
down_revision: Union[str, None] = '5a93f307f84e'
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
