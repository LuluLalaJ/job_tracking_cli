"""add job model

Revision ID: e706138ed21e
Revises: 3d464c8668b2
Create Date: 2023-05-15 09:42:43.677496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e706138ed21e'
down_revision = '3d464c8668b2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs',
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('job_title', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('salary_in_usd', sa.Integer(), nullable=True),
    sa.Column('remote', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('job_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jobs')
    # ### end Alembic commands ###
