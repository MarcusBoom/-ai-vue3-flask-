"""empty message

Revision ID: e6991915f92f
Revises: f6a06d2b7f4f
Create Date: 2024-06-20 11:07:14.101159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6991915f92f'
down_revision = 'f6a06d2b7f4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('chat_models', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_models', schema=None) as batch_op:
        batch_op.drop_column('url')

    op.drop_table('roles')
    # ### end Alembic commands ###
