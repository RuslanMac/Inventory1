"""first migrate

Revision ID: 9de8eaf69154
Revises: 
Create Date: 2020-07-17 23:09:11.469048

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '9de8eaf69154'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Objects')
    op.drop_table('Placement')
    op.drop_table('sysdiagrams')
    op.drop_table('Division')
    op.drop_table('Workers')
    op.drop_index('IX_Включает', table_name='Movement')
    op.drop_index('IX_Куда переместился', table_name='Movement')
    op.drop_index('IX_Откуда перемещение', table_name='Movement')
    op.drop_table('Movement')
    op.drop_table('Operation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Operation',
    sa.Column('operation_id', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=120, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('operation_id', name='Unique_Identifier2')
    )
    op.create_table('Movement',
    sa.Column('move_id', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=False),
    sa.Column('operation_date', sa.DATETIME(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=250, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('asinfo', sa.VARCHAR(length=250, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('operation_id', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=False),
    sa.Column('division_id', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=False),
    sa.Column('from_division_id', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=True),
    sa.Column('oid', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['division_id'], ['Division.division_id'], name='Откуда перемещение'),
    sa.ForeignKeyConstraint(['from_division_id'], ['Division.division_id'], name='Куда переместился'),
    sa.ForeignKeyConstraint(['oid'], ['Objects.oid'], name='Осуществляет перемещение'),
    sa.ForeignKeyConstraint(['operation_id'], ['Operation.operation_id'], name='Включает'),
    sa.PrimaryKeyConstraint('move_id', 'oid', name='Unique_Identifier1')
    )
    op.create_index('IX_Откуда перемещение', 'Movement', ['division_id'], unique=False)
    op.create_index('IX_Куда переместился', 'Movement', ['from_division_id'], unique=False)
    op.create_index('IX_Включает', 'Movement', ['operation_id'], unique=False)
    op.create_table('Workers',
    sa.Column('worker_id', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=False),
    sa.Column('login', sa.VARCHAR(length=25, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=255, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('token', sa.VARCHAR(length=35, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('token_expiration', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('worker_id', name='PK_Workers')
    )
    op.create_table('Division',
    sa.Column('division_id', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=120, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('division_id', name='Unique_Identifier4')
    )
    op.create_table('sysdiagrams',
    sa.Column('name', sa.NVARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('principal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('diagram_id', sa.INTEGER(), autoincrement=True, nullable=False, mssql_identity_start=1, mssql_identity_increment=1),
    sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('definition', mssql.VARBINARY(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B61E4F4322C')
    )
    op.create_table('Placement',
    sa.Column('placement_id', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=120, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('division_id', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['division_id'], ['Division.division_id'], name='Состоит из'),
    sa.PrimaryKeyConstraint('division_id', 'placement_id', name='Unique_Identifier5')
    )
    op.create_table('Objects',
    sa.Column('oid', mssql.UNIQUEIDENTIFIER(), server_default=sa.text('(newid())'), autoincrement=False, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=120, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('barcode', sa.VARCHAR(length=15, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('inv_number', sa.VARCHAR(length=100, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=150, collation='Cyrillic_General_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('asstatus', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('oid', name='Unique_Identifier3')
    )
    # ### end Alembic commands ###