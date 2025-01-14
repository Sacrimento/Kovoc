"""create vocabulary table

Revision ID: f1b801412871
Revises:
Create Date: 2025-01-14 01:20:16.338949

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1b801412871"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vocabulary",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("english", sa.Unicode(255), nullable=False),
        sa.Column("korean", sa.Unicode(255), nullable=False),
    )
    op.create_unique_constraint("uq_translation", "vocabulary", ["english", "korean"])


def downgrade() -> None:
    op.drop_table("vocabulary")
