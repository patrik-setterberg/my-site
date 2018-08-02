"""link_text in portf_project

Revision ID: ef6df75fd7c5
Revises: fb800a6e144c
Create Date: 2018-08-01 00:38:40.969726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef6df75fd7c5'
down_revision = 'fb800a6e144c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('portf_project', sa.Column('link_text', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('portf_project', 'link_text')
    # ### end Alembic commands ###