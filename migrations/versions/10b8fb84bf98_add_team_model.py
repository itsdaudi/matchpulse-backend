"""Add Team model

Revision ID: 10b8fb84bf98
Revises: b102464f1f0e
Create Date: 2026-08-09 22:34:39.751268

"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision = "10b8fb84bf98"
down_revision = "b102464f1f0e"
branch_labels = None
depends_on = None


def upgrade():
    # Create the teams table.
    #
    # Each team belongs to one league through league_id.
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("league_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("short_name", sa.String(length=20), nullable=True),
        sa.Column("logo", sa.String(length=255), nullable=True),
        sa.Column("stadium", sa.String(length=150), nullable=True),

        # Connect teams to the leagues table.
        sa.ForeignKeyConstraint(
            ["league_id"],
            ["leagues.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    # Remove the teams table when rolling back this migration.
    op.drop_table("teams")