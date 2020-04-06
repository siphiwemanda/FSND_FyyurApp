"""empty message

Revision ID: 866c996e988c
Revises: dee1258a4dd9
Create Date: 2020-04-05 09:40:28.697596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '866c996e988c'
down_revision = 'dee1258a4dd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###