"""empty message

Revision ID: bc382a38596b
Revises: be17a4b27fff
Create Date: 2024-03-18 12:23:28.207593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc382a38596b'
down_revision = 'be17a4b27fff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('HelloWorld')
    with op.batch_alter_table('Balances', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Balances', schema=None) as batch_op:
        batch_op.drop_column('balance')

    op.create_table('HelloWorld',
    sa.Column('uuid', sa.VARCHAR(length=48, collation='Latin1_General_CI_AI'), autoincrement=False, nullable=False),
    sa.Column('name', sa.NVARCHAR(collation='Latin1_General_CI_AI'), autoincrement=False, nullable=False),
    sa.Column('created_at', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.Column('updated_at', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('uuid', name='PK__HelloWor__7F427930B07DE765')
    )
    # ### end Alembic commands ###
