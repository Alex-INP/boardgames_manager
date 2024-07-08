"""empty message

Revision ID: 4b18eb9795fd
Revises: 401f1eddccf1
Create Date: 2024-07-08 14:19:52.461288

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4b18eb9795fd"
down_revision: Union[str, None] = "401f1eddccf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "user_roles", ["name"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_roles", type_="unique")
    # ### end Alembic commands ###