"""character

Revision ID: 19df07e120e5
Revises: e45d179078b7
Create Date: 2018-09-13 20:04:34.087982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19df07e120e5'
down_revision = 'e45d179078b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('race', sa.String(length=64), nullable=True),
    sa.Column('sub_race', sa.String(length=64), nullable=True),
    sa.Column('char_class', sa.String(length=64), nullable=True),
    sa.Column('sub_class', sa.String(length=64), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('party', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_character_name'), 'character', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_character_name'), table_name='character')
    op.drop_table('character')
    # ### end Alembic commands ###