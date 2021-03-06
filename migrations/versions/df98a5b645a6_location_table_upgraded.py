"""location table upgraded

Revision ID: df98a5b645a6
Revises: 040778c46855
Create Date: 2020-09-02 10:15:05.675030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df98a5b645a6'
down_revision = '040778c46855'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.drop_column('state')
        batch_op.drop_column('place_details')
        batch_op.drop_column('district')
        batch_op.drop_column('ward_no')
        batch_op.drop_column('municipality')

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('district', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('municipality', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('place_details', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('ward_no', sa.Integer(), nullable=True))

    with op.batch_alter_table('tutor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('district', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('full_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('municipality', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('place_details', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('ward_no', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tutor', schema=None) as batch_op:
        batch_op.drop_column('ward_no')
        batch_op.drop_column('state')
        batch_op.drop_column('place_details')
        batch_op.drop_column('municipality')
        batch_op.drop_column('full_name')
        batch_op.drop_column('district')

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('ward_no')
        batch_op.drop_column('state')
        batch_op.drop_column('place_details')
        batch_op.drop_column('municipality')
        batch_op.drop_column('district')

    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.add_column(sa.Column('municipality', sa.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('ward_no', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('district', sa.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('place_details', sa.VARCHAR(length=64), nullable=True))
        batch_op.add_column(sa.Column('state', sa.VARCHAR(length=64), nullable=True))

    # ### end Alembic commands ###
