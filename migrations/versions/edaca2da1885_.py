"""empty message

Revision ID: edaca2da1885
Revises: 28b653d3d0ac
Create Date: 2023-07-12 00:44:08.374146

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'edaca2da1885'
down_revision = '28b653d3d0ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Favoritos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Favoritos',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Favoritos_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planets_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('creation_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['People.id'], name='Favoritos_people_id_fkey'),
    sa.ForeignKeyConstraint(['planets_id'], ['Planets.id'], name='Favoritos_planets_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Favoritos_pkey')
    )
    # ### end Alembic commands ###
