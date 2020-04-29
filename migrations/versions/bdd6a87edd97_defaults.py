"""defaults

Revision ID: bdd6a87edd97
Revises: a895baecaf2f
Create Date: 2020-04-29 01:27:40.344665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdd6a87edd97'
down_revision = 'a895baecaf2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'familyName',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'givenName',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'givenName',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'familyName',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###