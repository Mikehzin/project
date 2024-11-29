"""empty message

Revision ID: 60dc60bd91d7
Revises: 6ec62e60b14c
Create Date: 2024-01-11 12:30:48.943795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60dc60bd91d7'
down_revision = '6ec62e60b14c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_online', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_online')
    # ### end Alembic commands ###
