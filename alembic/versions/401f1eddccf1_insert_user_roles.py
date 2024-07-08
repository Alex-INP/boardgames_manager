"""insert_user_roles

Revision ID: 401f1eddccf1
Revises: eb0f5867387d
Create Date: 2024-06-26 13:26:05.349595

"""

from typing import Sequence, Union

from sqlalchemy import DateTime, Integer, String, column, table

from alembic import op
from src.utils import get_now_utc

# revision identifiers, used by Alembic.
revision: str = "401f1eddccf1"
down_revision: Union[str, None] = "eb0f5867387d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "eb0f5867387d"


ur_table = table(
    "user_roles",
    column("id", Integer),
    column("name", String),
    column("created", DateTime),
)


def upgrade() -> None:
    op.bulk_insert(
        ur_table,
        [
            {
                "id": 1,
                "name": "Admin",
                "created": get_now_utc(),
            },
            {
                "id": 2,
                "name": "User",
                "created": get_now_utc(),
            },
        ],
    )


def downgrade() -> None:
    pass
