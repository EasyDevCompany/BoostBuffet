"""add_url_to_post

Revision ID: e70e210f1542
Revises: 911853340766
Create Date: 2023-02-02 20:30:04.523761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e70e210f1542'
down_revision = '911853340766'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('url_to_post', sa.String(length=500), nullable=True))
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
    op.drop_column('posts', 'url_to_post')
    # ### end Alembic commands ###