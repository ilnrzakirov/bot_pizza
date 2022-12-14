"""

Revision ID: 6cb196e35aa8
Revises: b14e7fb5dd17
Create Date: 2022-11-26 14:32:01.363235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cb196e35aa8'
down_revision = 'b14e7fb5dd17'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association_mod_basket',
    sa.Column('baskets_id', sa.Integer(), nullable=True),
    sa.Column('modifications_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['baskets_id'], ['baskets.id'], ),
    sa.ForeignKeyConstraint(['modifications_id'], ['modifications.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_mod_basket')
    # ### end Alembic commands ###
