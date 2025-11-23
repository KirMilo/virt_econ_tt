"""add_mock_users

Revision ID: 9c30b1d60929
Revises: d89e71f80d48
Create Date: 2025-11-23 15:14:11.702076

"""
import os
import sys
from datetime import timezone, datetime
from random import randint
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

src_path = os.path.join(os.path.dirname(__file__), "..", "..", "src")
src_path = os.path.abspath(src_path)
sys.path.insert(0, src_path)

from core.db.models import User


# revision identifiers, used by Alembic.
revision: str = '9c30b1d60929'
down_revision: Union[str, Sequence[str], None] = 'd89e71f80d48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    mock_users = [
        {
            "id": i,
            "username": f"mock_user_{i}",
            "email": f"mock_user_{i}@example.com",
            "balance": randint(500, 1000),
            "created_at": datetime.now(timezone.utc)
        } for i in range(1, 11)
    ]
    op.bulk_insert(User.__table__, mock_users)  # noqa

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DELETE FROM users "
        "WHERE username LIKE 'mock_user_%';"
    )
