"""last_edit in blogposts

Revision ID: 335b562d642c
Revises: d9541df700e4
Create Date: 2018-06-20 14:40:51.830102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '335b562d642c'
down_revision = 'd9541df700e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_post', sa.Column('last_edit', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_blog_post_last_edit'), 'blog_post', ['last_edit'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_post_last_edit'), table_name='blog_post')
    op.drop_column('blog_post', 'last_edit')
    # ### end Alembic commands ###
