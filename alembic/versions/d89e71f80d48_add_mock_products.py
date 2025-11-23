"""add_mock_products

Revision ID: d89e71f80d48
Revises: 72584ddb92ae
Create Date: 2025-11-23 12:52:43.156510

"""
import os
import sys

from typing import Sequence, Union
from random import randint
from alembic import op

src_path = os.path.join(os.path.dirname(__file__), "..", "..", "src")
src_path = os.path.abspath(src_path)
sys.path.insert(0, src_path)

from core.db.models import Product
from core.enums import ProductTypeEnum

# revision identifiers, used by Alembic.
revision: str = 'd89e71f80d48'
down_revision: Union[str, Sequence[str], None] = '72584ddb92ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    consumable = [
        {
            "id": i,
            "name": f"cons_product_{i}",
            "description": f"cons_product_description_{i}",
            "price": randint(1, 20),
            "type": ProductTypeEnum.CONSUMABLE,
        } for i in range(1, 21)
    ]
    offset = len(consumable)
    permanent = [
        {
            "id": i + offset,
            "name": f"perm_product_{i}",
            "description": f"perm_product_description_{i}",
            "price": randint(5, 20),
            "type": ProductTypeEnum.PERMANENT,
        } for i in range(1, 21)
    ]
    op.bulk_insert(Product.__table__, consumable + permanent)  # NOQA

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DELETE FROM products "
        "WHERE name LIKE 'cons_product_%' OR name LIKE 'perm_product_%';"
    )
