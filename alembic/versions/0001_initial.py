# alembic/versions/0001_initial.py
"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2025-01-01 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), index=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float()),
    )

def downgrade():
    op.drop_table('items')
    op.drop_table('users')