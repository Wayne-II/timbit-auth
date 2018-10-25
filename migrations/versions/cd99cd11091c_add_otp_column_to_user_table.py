"""add otp column to user table

Revision ID: cd99cd11091c
Revises: 4e3b3d4fed1a
Create Date: 2018-10-20 11:37:03.664707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd99cd11091c'
down_revision = '4e3b3d4fed1a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column( 'otp_secret', sa.String, nullable=False )
    )


def downgrade():
    pass
