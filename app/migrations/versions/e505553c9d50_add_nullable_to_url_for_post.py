"""add_nullable_to_url_for_post

Revision ID: e505553c9d50
Revises: e70e210f1542
Create Date: 2023-02-02 20:34:59.346015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e505553c9d50'
down_revision = 'e70e210f1542'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###