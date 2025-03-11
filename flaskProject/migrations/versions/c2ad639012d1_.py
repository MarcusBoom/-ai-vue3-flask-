"""empty message

Revision ID: c2ad639012d1
Revises: e6991915f92f
Create Date: 2024-06-20 11:08:00.298177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2ad639012d1'
down_revision = 'e6991915f92f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('department', sa.String(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('department_pinyin', sa.String(), nullable=True),
    sa.Column('department_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('department_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('department')
    # ### end Alembic commands ###
