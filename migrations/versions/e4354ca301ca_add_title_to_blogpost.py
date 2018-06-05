"""add title to blogpost

Revision ID: e4354ca301ca
Revises: 08ab55f57451
Create Date: 2018-06-05 20:17:02.800145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4354ca301ca'
down_revision = '08ab55f57451'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_post', sa.Column('title', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog_post', 'title')
    # ### end Alembic commands ###