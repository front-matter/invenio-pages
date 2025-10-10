#
# This file is part of Invenio.
# Copyright (C) 2025 University of Münster.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Add language and new uq."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "1737449793"
down_revision = "9fae3c5404d9"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # Get the connection and inspector
    conn = op.get_bind()
    inspector = inspect(conn)

    # Get existing columns and constraints
    pages_page_columns = [col["name"] for col in inspector.get_columns("pages_page")]
    pages_page_version_columns = [
        col["name"] for col in inspector.get_columns("pages_page_version")
    ]

    # Get existing unique constraints for pages_page
    existing_constraints = []
    try:
        constraints = inspector.get_unique_constraints("pages_page")
        existing_constraints = [constraint["name"] for constraint in constraints]
    except Exception:
        # Some databases might not support this, fallback to empty list
        existing_constraints = []

    # Drop old unique constraint if it exists
    if "uq_pages_page_url" in existing_constraints:
        op.drop_constraint(op.f("uq_pages_page_url"), "pages_page", type_="unique")

    # Add lang column to pages_page if it doesn't exist
    if "lang" not in pages_page_columns:
        op.add_column(
            "pages_page",
            sa.Column(
                "lang",
                sa.CHAR(length=2),
                server_default="en",
                nullable=False,
            ),
        )

    # Create new unique constraint if it doesn't exist
    if "uq_pages_page_url_lang" not in existing_constraints:
        op.create_unique_constraint(
            "uq_pages_page_url_lang", "pages_page", ["url", "lang"]
        )

    # Add lang column to pages_page_version if it doesn't exist
    if "lang" not in pages_page_version_columns:
        op.add_column(
            "pages_page_version",
            sa.Column(
                "lang",
                sa.CHAR(length=2),
                server_default="en",
                nullable=True,
            ),
        )


def downgrade():
    """Downgrade database."""
    # Get the connection and inspector
    conn = op.get_bind()
    inspector = inspect(conn)

    # Get existing columns and constraints
    pages_page_columns = [col["name"] for col in inspector.get_columns("pages_page")]
    pages_page_version_columns = [
        col["name"] for col in inspector.get_columns("pages_page_version")
    ]

    # Get existing unique constraints for pages_page
    existing_constraints = []
    try:
        constraints = inspector.get_unique_constraints("pages_page")
        existing_constraints = [constraint["name"] for constraint in constraints]
    except Exception:
        # Some databases might not support this, fallback to empty list
        existing_constraints = []

    # Drop lang column from pages_page_version if it exists
    if "lang" in pages_page_version_columns:
        op.drop_column("pages_page_version", "lang")

    # Drop new unique constraint if it exists
    if "uq_pages_page_url_lang" in existing_constraints:
        op.drop_constraint("uq_pages_page_url_lang", "pages_page", type_="unique")

    # Drop lang column from pages_page if it exists
    if "lang" in pages_page_columns:
        op.drop_column("pages_page", "lang")

    # Create old unique constraint if it doesn't exist
    if "uq_pages_page_url" not in existing_constraints:
        op.create_unique_constraint(op.f("uq_pages_page_url"), "pages_page", ["url"])
