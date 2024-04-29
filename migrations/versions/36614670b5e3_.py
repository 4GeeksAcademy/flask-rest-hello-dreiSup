"""empty message

Revision ID: 36614670b5e3
Revises: 
Create Date: 2024-04-29 17:18:35.138931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36614670b5e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('birth_year', sa.String(length=50), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.Column('characterDesc', sa.String(length=250), nullable=True),
    sa.Column('height', sa.String(length=20), nullable=True),
    sa.Column('mass', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('hair_color', sa.String(length=20), nullable=True),
    sa.Column('skin_color', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=400), nullable=False),
    sa.Column('climate', sa.String(length=400), nullable=False),
    sa.Column('diameter', sa.String(length=400), nullable=False),
    sa.Column('planetDesc', sa.String(length=400), nullable=False),
    sa.Column('rotation_period', sa.String(length=400), nullable=False),
    sa.Column('orbital_period', sa.String(length=400), nullable=False),
    sa.Column('gravity', sa.String(length=400), nullable=False),
    sa.Column('population', sa.String(length=400), nullable=False),
    sa.Column('terrain', sa.String(length=400), nullable=False),
    sa.Column('surface_water', sa.String(length=400), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('user')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
