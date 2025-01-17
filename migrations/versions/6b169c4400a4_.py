"""empty message

Revision ID: 6b169c4400a4
Revises: b99d05892264
Create Date: 2024-01-10 10:50:22.594811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b169c4400a4'
down_revision = 'b99d05892264'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logged',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.Column('cargo', sa.String(length=120), nullable=True),
    sa.Column('data_logon', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('data', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'data')
    op.drop_table('logged')
    # ### end Alembic commands ###
