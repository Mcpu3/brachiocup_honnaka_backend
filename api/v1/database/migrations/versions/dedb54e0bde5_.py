"""empty message

Revision ID: dedb54e0bde5
Revises: 
Create Date: 2024-03-09 17:31:57.723576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dedb54e0bde5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Helloworld',
    sa.Column('uuid', sa.String(length=48), nullable=False),
    sa.Column('name', sa.String(length=48), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Helloworld')
    # ### end Alembic commands ###