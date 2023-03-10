"""added bio to card model

Revision ID: 78b7206df770
Revises: f50e839fa4c1
Create Date: 2023-01-19 03:09:41.762748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78b7206df770'
down_revision = 'f50e839fa4c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('bio', sa.String(length=150), nullable=True))
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
    op.drop_column('cards', 'bio')
    # ### end Alembic commands ###
