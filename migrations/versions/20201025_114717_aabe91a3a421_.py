"""empty message

Revision ID: aabe91a3a421
Revises: 
Create Date: 2020-10-25 11:47:17.390273+09:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aabe91a3a421'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='登録日時'),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True, comment='最終更新日時'),
    sa.Column('email', sa.VARCHAR(length=254), nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###