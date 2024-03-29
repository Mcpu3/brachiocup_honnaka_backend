"""empty message

Revision ID: fbe3d73e17df
Revises: bc382a38596b
Create Date: 2024-03-18 15:13:43.890663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbe3d73e17df'
down_revision = 'bc382a38596b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('HelloWorld')
    with op.batch_alter_table('ItemPurchasingHistories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_uuid', sa.String(length=48), nullable=False))
        batch_op.create_foreign_key(None, 'Groups', ['group_uuid'], ['uuid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ItemPurchasingHistories', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('group_uuid')

    op.create_table('HelloWorld',
    sa.Column('uuid', sa.VARCHAR(length=48, collation='Latin1_General_CI_AI'), autoincrement=False, nullable=False),
    sa.Column('name', sa.NVARCHAR(collation='Latin1_General_CI_AI'), autoincrement=False, nullable=False),
    sa.Column('created_at', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.Column('updated_at', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('uuid', name='PK__HelloWor__7F427930E0AE7411')
    )
    # ### end Alembic commands ###
