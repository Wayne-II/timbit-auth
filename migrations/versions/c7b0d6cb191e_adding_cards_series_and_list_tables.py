"""adding cards series and list tables

Revision ID: c7b0d6cb191e
Revises: cd99cd11091c
Create Date: 2018-10-22 22:57:55.874275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7b0d6cb191e'
down_revision = 'cd99cd11091c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'card_series',
        sa.Column( 'id', sa.Integer, primary_key=True, autoincrement=True ),
        sa.Column( 'name', sa.String(256), unique=True, nullable=False ),
        sa.Column( 'path', sa.String(256), unique=True, nullable=False ),
        sa.Column( 'description', sa.String(4096), nullable=False )
    )
    op.create_table(
        'cards',
        sa.Column( 'id', sa.Integer, primary_key=True, autoincrement=True ),
        sa.Column( 'filename', sa.String(256), unique=True, nullable=False ),
        sa.Column( 'hash', sa.String(4096), nullable=False )
    )


def downgrade():
    pass
