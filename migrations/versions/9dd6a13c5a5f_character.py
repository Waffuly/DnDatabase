"""character

Revision ID: 9dd6a13c5a5f
Revises: 44e0f580efb6
Create Date: 2018-09-13 17:22:56.985188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dd6a13c5a5f'
down_revision = '44e0f580efb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('sub_class', sa.String(length=64), nullable=True))
    op.add_column('character', sa.Column('sub_race', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('character', 'sub_race')
    op.drop_column('character', 'sub_class')
    # ### end Alembic commands ###
