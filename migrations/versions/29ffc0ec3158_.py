"""empty message

Revision ID: 29ffc0ec3158
Revises: 
Create Date: 2020-11-19 15:47:11.552196

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '29ffc0ec3158'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rolename', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['trivia_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('trivia_user', sa.Column('tiempo', sa.Float(), nullable=True))
    op.drop_column('trivia_user', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trivia_user', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('trivia_user', 'tiempo')
    op.drop_table('role')
    # ### end Alembic commands ###