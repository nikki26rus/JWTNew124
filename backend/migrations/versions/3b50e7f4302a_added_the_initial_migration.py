"""Added the initial migration

Revision ID: 3b50e7f4302a
Revises: a4d52c58c3e9
Create Date: 2024-12-24 15:02:55.053820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b50e7f4302a'
down_revision: Union[str, None] = 'a4d52c58c3e9'
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
