"""actualizaciones producto

Revision ID: cbbb32890a54
Revises: 8e0fcda9f1f0
Create Date: 2025-05-05 11:44:04.308365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbbb32890a54'
down_revision = '8e0fcda9f1f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
