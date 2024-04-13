"""removed some

Revision ID: 5187ebd49962
Revises: 7c09636eb885
Create Date: 2024-03-29 20:52:34.991926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5187ebd49962'
down_revision = '7c09636eb885'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cycledata', schema=None) as batch_op:
        batch_op.alter_column('creator_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('usid', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cycledata', schema=None) as batch_op:
        batch_op.create_foreign_key('usid', 'user', ['creator_id'], ['id'])
        batch_op.alter_column('creator_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###