"""empty message

Revision ID: 7e7f9ee1a596
Revises: 6b169c4400a4
Create Date: 2024-01-10 10:58:37.341140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e7f9ee1a596'
down_revision = '6b169c4400a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logged', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'logged', 'users', ['user_id'], ['id'])
    op.drop_column('logged', 'username')
    op.drop_column('logged', 'cargo')
    op.drop_column('logged', 'email')
    op.drop_column('logged', 'password')
    op.drop_column('logged', 'permission')
    op.drop_column('logged', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logged', sa.Column('name', sa.VARCHAR(length=64, collation='Latin1_General_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('logged', sa.Column('permission', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('logged', sa.Column('password', sa.VARCHAR(length=50, collation='Latin1_General_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('logged', sa.Column('email', sa.VARCHAR(length=120, collation='Latin1_General_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('logged', sa.Column('cargo', sa.VARCHAR(length=120, collation='Latin1_General_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('logged', sa.Column('username', sa.VARCHAR(length=64, collation='Latin1_General_CI_AS'), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'logged', type_='foreignkey')
    op.drop_column('logged', 'user_id')
    # ### end Alembic commands ###
