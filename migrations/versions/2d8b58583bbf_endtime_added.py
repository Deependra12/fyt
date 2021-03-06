"""endtime added

Revision ID: 2d8b58583bbf
Revises: 84a821e76f5f
Create Date: 2020-09-23 09:13:17.965107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d8b58583bbf'
down_revision = '84a821e76f5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mycourse', schema=None) as batch_op:
        batch_op.add_column(sa.Column('endtime', sa.Time(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mycourse', schema=None) as batch_op:
        batch_op.drop_column('endtime')

    # ### end Alembic commands ###
