"""empty message

Revision ID: 09521b733f44
Revises: 9f5a49894627
Create Date: 2017-03-13 20:41:31.991064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09521b733f44'
down_revision = '9f5a49894627'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'profiles_userid_key', 'profiles', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(u'profiles_userid_key', 'profiles', ['userid'])
    # ### end Alembic commands ###
