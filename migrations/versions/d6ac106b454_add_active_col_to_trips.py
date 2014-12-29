"""add active col to trips

Revision ID: d6ac106b454
Revises: 33f1750e0376
Create Date: 2014-12-27 23:26:32.355441

"""

# revision identifiers, used by Alembic.
revision = 'd6ac106b454'
down_revision = '33f1750e0376'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trips', sa.Column('active', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trips', 'active')
    ### end Alembic commands ###
