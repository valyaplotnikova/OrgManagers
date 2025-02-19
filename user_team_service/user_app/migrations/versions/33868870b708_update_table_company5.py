"""update_table_company5

Revision ID: 33868870b708
Revises: 07eb1dcd159f
Create Date: 2025-02-07 16:05:18.512668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33868870b708'
down_revision: Union[str, None] = '07eb1dcd159f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('structures_company_id_fkey', 'structures', type_='foreignkey')
    op.create_foreign_key(None, 'structures', 'companys', ['company_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'structures', type_='foreignkey')
    op.create_foreign_key('structures_company_id_fkey', 'structures', 'companys', ['company_id'], ['id'])
    # ### end Alembic commands ###
