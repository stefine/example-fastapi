"""add tel into User

Revision ID: 929bcfb9ef65
Revises: 
Create Date: 2023-02-19 18:13:02.828969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '929bcfb9ef65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
