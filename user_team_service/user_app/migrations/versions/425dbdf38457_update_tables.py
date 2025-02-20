"""update_tables

Revision ID: 425dbdf38457
Revises: 79df1c899db0
Create Date: 2025-02-07 11:49:57.107052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '425dbdf38457'
down_revision: Union[str, None] = '79df1c899db0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('company_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'companys', ['company_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'company_id')
