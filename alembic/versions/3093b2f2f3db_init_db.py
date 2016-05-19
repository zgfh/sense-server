"""init db

Revision ID: 3093b2f2f3db
Revises: 
Create Date: 2016-05-19 18:29:26.674498

"""

# revision identifiers, used by Alembic.
revision = '3093b2f2f3db'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "post",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("read_ts", sa.TIMESTAMP),
        sa.Column("is_favorite", sa.BOOLEAN)
    )

    def downgrade():
        op.drop_table("post")
