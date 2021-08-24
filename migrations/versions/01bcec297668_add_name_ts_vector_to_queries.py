"""add name ts_vector to Queries

Revision ID: 01bcec297668
Revises: 052ea23ef537
Create Date: 2021-08-24 10:56:00.520911

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as su
import sqlalchemy_searchable as ss


# revision identifiers, used by Alembic.
revision = '01bcec297668'
down_revision = '052ea23ef537'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    op.add_column("queries", sa.Column("search_vector_flat", su.TSVectorType()))
    op.create_index(
        "ix_queries_search_vector_flat",
        "queries",
        ["search_vector_flat"],
        unique=False,
        postgresql_using="gin",
    )
    ss.sync_trigger(conn, "queries", "search_vector_flat", ["name"])


def downgrade():
    conn = op.get_bind()

    ss.drop_trigger(conn, "queries", "search_vector_flat")
    op.drop_index("ix_queries_search_vector_flat", table_name="queries")
    op.drop_column("queries", "search_vector_flat")