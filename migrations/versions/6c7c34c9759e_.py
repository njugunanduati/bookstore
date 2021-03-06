"""empty message

Revision ID: 6c7c34c9759e
Revises: df9cb30c76b1
Create Date: 2021-04-11 10:39:05.945484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c7c34c9759e'
down_revision = 'df9cb30c76b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_type',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('rent_charge', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('book', sa.Column('book_type', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'book', 'book_type', ['book_type'], ['id'])
    op.drop_column('book', 'rent_charge')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('rent_charge', sa.REAL(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_column('book', 'book_type')
    op.drop_table('book_type')
    # ### end Alembic commands ###
