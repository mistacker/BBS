"""empty message

Revision ID: 54597d3ab5e3
Revises: 706328b13017
Create Date: 2017-03-15 14:25:48.252000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '54597d3ab5e3'
down_revision = '706328b13017'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('_password', sa.String(length=100), nullable=False))
    op.alter_column('cms_user', 'join_time',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_column('cms_user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('password', mysql.VARCHAR(length=100), nullable=False))
    op.alter_column('cms_user', 'join_time',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.drop_column('cms_user', '_password')
    # ### end Alembic commands ###
