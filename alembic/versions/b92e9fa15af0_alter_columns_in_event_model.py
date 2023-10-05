"""Alter columns in Event model

Revision ID: b92e9fa15af0
Revises: ccb316d070f9
Create Date: 2023-09-30 10:29:06.957285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b92e9fa15af0'
down_revision: Union[str, None] = 'ccb316d070f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'longitude',
               existing_type=sa.NUMERIC(precision=9, scale=6),
               type_=sa.Numeric(precision=12, scale=6),
               existing_nullable=False)
    op.alter_column('event', 'latitude',
               existing_type=sa.NUMERIC(precision=8, scale=6),
               type_=sa.Numeric(precision=12, scale=6),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'latitude',
               existing_type=sa.Numeric(precision=12, scale=6),
               type_=sa.NUMERIC(precision=8, scale=6),
               existing_nullable=False)
    op.alter_column('event', 'longitude',
               existing_type=sa.Numeric(precision=12, scale=6),
               type_=sa.NUMERIC(precision=9, scale=6),
               existing_nullable=False)
    # ### end Alembic commands ###