"""insert_user_roles

Revision ID: 401f1eddccf1
Revises: eb0f5867387d
Create Date: 2024-06-26 13:26:05.349595

"""

import datetime
from typing import Sequence, Union

from alembic import op
from sqlalchemy import table, column, Integer, String, DateTime

# revision identifiers, used by Alembic.
revision: str = "401f1eddccf1"
down_revision: Union[str, None] = "eb0f5867387d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
                "created": datetime.datetime.now(),
            },
            {
                "id": 2,
                "name": "User",
                "created": datetime.datetime.now(),
            },
        ],
    )


def downgrade() -> None:
    pass
