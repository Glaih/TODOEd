"""tablename `task` -> `tasks`

Revision ID: 9cad93347e3c
Revises: 61a4eba498cf
Create Date: 2021-04-13 15:16:33.852560

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9cad93347e3c'
down_revision = '61a4eba498cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('text', sa.String(length=180), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.drop_table('task')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('task_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('text', sa.VARCHAR(length=180), autoincrement=False, nullable=False),
    sa.Column('deadline', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='task_user_id_fkey'),
    sa.PrimaryKeyConstraint('task_id', name='task_pkey')
    )
    op.drop_table('tasks')
    # ### end Alembic commands ###
