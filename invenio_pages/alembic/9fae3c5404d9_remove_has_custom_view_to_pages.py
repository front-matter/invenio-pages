#
# This file is part of Invenio.
# Copyright (C) 2016-2024 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remove has_custom_view from pages."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "9fae3c5404d9"
down_revision = "b0f93ca4a147"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # Get the connection and inspector
    conn = op.get_bind()
    inspector = inspect(conn)

    # Check if the columns exist before dropping them
    pages_page_columns = [col["name"] for col in inspector.get_columns("pages_page")]
    pages_page_version_columns = [
        col["name"] for col in inspector.get_columns("pages_page_version")
    ]

    # Drop the column from pages_page if it exists
    if "has_custom_view" in pages_page_columns:
        op.drop_column("pages_page", "has_custom_view")

    # Drop the column from pages_page_version if it exists
    if "has_custom_view" in pages_page_version_columns:
        op.drop_column("pages_page_version", "has_custom_view")
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # Get the connection and inspector
    conn = op.get_bind()
    inspector = inspect(conn)

    # Check if the columns exist before adding them
    pages_page_columns = [col["name"] for col in inspector.get_columns("pages_page")]
    pages_page_version_columns = [
        col["name"] for col in inspector.get_columns("pages_page_version")
    ]

    # Add the column to pages_page if it doesn't exist
    if "has_custom_view" not in pages_page_columns:
        op.add_column(
            "pages_page",
            sa.Column(
                "has_custom_view",
                sa.Boolean(),
                nullable=False,
                server_default=sa.sql.expression.literal(False),
                default=False,
            ),
        )

    # Add the column to pages_page_version if it doesn't exist
    if "has_custom_view" not in pages_page_version_columns:
        op.add_column(
            "pages_page_version",
            sa.Column(
                "has_custom_view",
                sa.Boolean(),
                nullable=True,
                server_default=sa.sql.expression.literal(False),
                default=False,
            ),
        )
    # ### end Alembic commands ###
