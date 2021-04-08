"""empty message

Revision ID: df9cb30c76b1
Revises: be69f8262276
Create Date: 2021-04-08 17:08:40.504084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df9cb30c76b1'
down_revision = 'be69f8262276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.add_column('book', sa.Column('author', sa.Integer(), nullable=True))
    op.drop_constraint('book_author_id_fkey', 'book', type_='foreignkey')
    op.create_foreign_key(None, 'book', 'author', ['author'], ['id'])
    op.drop_column('book', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.create_foreign_key('book_author_id_fkey', 'book', 'author', ['author_id'], ['id'])
    op.drop_column('book', 'author')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
