"""2

Revision ID: 753781f26f85
Revises: b126cb40e9b8
Create Date: 2025-01-25 17:22:07.538792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '753781f26f85'
down_revision = 'b126cb40e9b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('minutes_to_complete',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('minutes_to_complete',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
