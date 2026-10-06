"""initial migration

Revision ID: a501e789c4e5
Revises: 
Create Date: 2026-10-06 11:04:05.497288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a501e789c4e5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create tables for the infrastructure monitoring system

    # --- Media table ---

    op.create_table(
        "media",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.Integer(), nullable=True),
        sa.Column("media_type", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("mime_type", sa.String(), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_media_id"), "media", ["id"], unique=False
    )

    # --- Analysis table ---

    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("media_type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("issue_type", sa.String(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("severity", sa.String(), nullable=True),
        sa.Column("priority", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("recommended_action", sa.String(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("location_name", sa.String(), nullable=True),
        sa.Column("location_source", sa.String(), nullable=True),
        sa.Column("video_timestamp", sa.String(), nullable=True),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_analyses_id"), "analyses", ["id"], unique=False
    )

    # --- InfrastructureReport table ---

    op.create_table(
        "infra_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.Integer(), sa.ForeignKey("analyses.id"), nullable=True),
        sa.Column("media_type", sa.String(), nullable=False),
        sa.Column("media_url", sa.String(), nullable=True),
        sa.Column("issue_type", sa.String(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("recommended_action", sa.String(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("location_name", sa.String(), nullable=True),
        sa.Column("location_source", sa.String(), nullable=True),
        sa.Column("video_timestamp", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_infra_reports_id"), "infra_reports", ["id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("infra_reports")
    op.drop_table("analyses")
    op.drop_table("media")