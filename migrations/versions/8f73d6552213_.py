"""empty message

Revision ID: 8f73d6552213
Revises: 65896658e6a7
Create Date: 2017-03-22 10:46:11.672000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f73d6552213'
down_revision = '65896658e6a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('is_live', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cms_user', 'is_live')
    # ### end Alembic commands ###
