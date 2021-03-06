"""email confirmation field added

Revision ID: f041042f102d
Revises: 2d8b58583bbf
Create Date: 2020-10-01 15:54:14.220941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f041042f102d'
down_revision = '2d8b58583bbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed_account', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('confirmed_account')

    # ### end Alembic commands ###
