"""empty message

Revision ID: 396a8fdb488a
Revises: d56a1251493b
Create Date: 2024-06-26 16:55:09.621709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396a8fdb488a'
down_revision = 'd56a1251493b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('department', schema=None) as batch_op:
        batch_op.drop_column('phone')
        batch_op.drop_column('email')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
