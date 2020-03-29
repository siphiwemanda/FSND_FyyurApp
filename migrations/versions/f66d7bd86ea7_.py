"""empty message

Revision ID: f66d7bd86ea7
Revises: c8c5bf2e1395
Create Date: 2020-03-26 15:27:18.364834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f66d7bd86ea7'
down_revision = 'c8c5bf2e1395'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'image_link')
    op.drop_column('artist', 'genres')
    op.drop_column('artist', 'facebook_link')
    op.drop_column('artist', 'phone')
    op.drop_column('artist', 'city')
    op.drop_column('artist', 'state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###