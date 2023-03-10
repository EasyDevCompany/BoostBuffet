"""added channel link to post

Revision ID: 5833a48542b0
Revises: 911853340766
Create Date: 2023-02-07 15:00:05.253741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5833a48542b0'
down_revision = '911853340766'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('channel_link', sa.String(), nullable=True))
    op.alter_column('telegramusers', 'raiting',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=1),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('telegramusers', 'raiting',
               existing_type=sa.Float(precision=1),
               type_=sa.REAL(),
               existing_nullable=True)
    op.drop_column('posts', 'channel_link')
    # ### end Alembic commands ###
