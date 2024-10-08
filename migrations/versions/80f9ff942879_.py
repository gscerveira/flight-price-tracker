"""empty message

Revision ID: 80f9ff942879
Revises: 
Create Date: 2024-09-30 00:30:36.655631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80f9ff942879'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flights',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('origin', sa.String(length=50), nullable=False),
    sa.Column('destination', sa.String(length=50), nullable=False),
    sa.Column('departure_date', sa.Date(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('flight_preferences',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('flight_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_records',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('flight_id', sa.UUID(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('price_records')
    op.drop_table('flight_preferences')
    op.drop_table('users')
    op.drop_table('flights')
    # ### end Alembic commands ###
