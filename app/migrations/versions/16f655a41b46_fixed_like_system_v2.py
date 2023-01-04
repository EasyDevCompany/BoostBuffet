"""fixed_like_system_v2

Revision ID: 16f655a41b46
Revises: 7d1c52a13e43
Create Date: 2023-01-04 23:20:52.102129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '16f655a41b46'
down_revision = '7d1c52a13e43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_likes_id', table_name='likes')
    op.drop_table('likes')
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
    op.create_table('likes',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('post_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('like_author', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('status', postgresql.ENUM('liked', 'unliked', name='likestatus'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['like_author'], ['telegramusers.id'], name='likes_like_author_fkey'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='likes_post_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='likes_pkey')
    )
    op.create_index('ix_likes_id', 'likes', ['id'], unique=False)
    # ### end Alembic commands ###