"""empty message

Revision ID: 47175b038730
Revises: 466ce16ba2a2
Create Date: 2024-11-05 22:04:50.222469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47175b038730'
down_revision = '466ce16ba2a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
