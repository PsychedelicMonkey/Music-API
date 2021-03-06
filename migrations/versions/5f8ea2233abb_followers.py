"""followers

Revision ID: 5f8ea2233abb
Revises: 91de51cf5385
Create Date: 2021-02-07 15:49:11.983794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f8ea2233abb'
down_revision = '91de51cf5385'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
