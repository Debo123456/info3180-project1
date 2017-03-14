"""empty message

Revision ID: 82a6d55b617b
Revises: 09521b733f44
Create Date: 2017-03-13 20:42:53.986285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82a6d55b617b'
down_revision = '09521b733f44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('profiles', 'userid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('userid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('profiles', 'id')
    # ### end Alembic commands ###