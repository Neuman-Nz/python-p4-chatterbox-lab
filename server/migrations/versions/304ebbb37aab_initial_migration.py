"""Initial migration

Revision ID: 304ebbb37aab
Revises: 2ed03edd40ad
Create Date: 2024-04-24 14:59:10.938213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304ebbb37aab'
down_revision = '2ed03edd40ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('username', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('username')
        batch_op.drop_column('body')

    # ### end Alembic commands ###