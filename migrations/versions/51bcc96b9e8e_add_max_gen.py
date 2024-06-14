"""add max gen

Revision ID: 51bcc96b9e8e
Revises: 0d60c5a1c524
Create Date: 2024-06-02 11:30:32.428476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51bcc96b9e8e'
down_revision: Union[str, None] = '0d60c5a1c524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('gen_qnt', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'gen_qnt')
    # ### end Alembic commands ###