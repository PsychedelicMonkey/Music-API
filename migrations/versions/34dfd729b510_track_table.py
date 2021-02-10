"""track table

Revision ID: 34dfd729b510
Revises: 5f8ea2233abb
Create Date: 2021-02-10 13:47:20.444583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34dfd729b510'
down_revision = '5f8ea2233abb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track_no', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.Column('runtime', sa.DateTime(), nullable=True),
    sa.Column('released', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track')
    # ### end Alembic commands ###