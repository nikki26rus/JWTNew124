"""Added the initial migration

Revision ID: 759ddae84f7d
Revises: 726ccdf4681b
Create Date: 2024-12-27 09:25:46.930659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '759ddae84f7d'
down_revision: Union[str, None] = '726ccdf4681b'
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