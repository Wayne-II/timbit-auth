"""create blacklist_tokens table

Revision ID: 4e3b3d4fed1a
Revises:
Create Date: 2018-10-13 20:44:06.881518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e3b3d4fed1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'blacklist_tokens',
        sa.Column( 'id', sa.Integer, primary_key=True, autoincrement=True ),
        sa.Column( 'token', sa.String(500), unique=True, nullable=False ),
        sa.Column( 'blacklisted_on', sa.DateTime, nullable=False )
    )

def downgrade():
    pass
