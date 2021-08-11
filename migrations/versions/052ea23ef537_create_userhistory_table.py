"""create UserHistory table

Revision ID: 052ea23ef537
Revises: 89bc7873a3e0
Create Date: 2021-08-10 13:27:19.951536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '052ea23ef537'
down_revision = '89bc7873a3e0'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "UserHistory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("query_string", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("UserHistory")
