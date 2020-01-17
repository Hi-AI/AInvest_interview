# coding: utf-8
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class AuthGroup(db.Model):
    __tablename__ = 'auth_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)



class AuthGroupPermission(db.Model):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        db.Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False, index=True)
    permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthGroupPermission.group_id == AuthGroup.id', backref='auth_group_permissions')
    permission = db.relationship('AuthPermission', primaryjoin='AuthGroupPermission.permission_id == AuthPermission.id', backref='auth_group_permissions')



class AuthPermission(db.Model):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        db.Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename'),
    )

    id = db.Column(db.Integer, primary_key=True)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id'), nullable=False, index=True)
    codename = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    content_type = db.relationship('DjangoContentType', primaryjoin='AuthPermission.content_type_id == DjangoContentType.id', backref='auth_permissions')



class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime)
    is_superuser = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    telephone = db.Column(db.String(30))
    originate = db.Column(db.String(30))
    is_pay = db.Column(db.Boolean, nullable=False)
    register_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    login_num = db.Column(db.Integer, nullable=False)



class ClientGroup(db.Model):
    __tablename__ = 'client_groups'
    __table_args__ = (
        db.Index('client_groups_client_id_group_id_b189a7bd_uniq', 'client_id', 'group_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.ForeignKey('client.id'), nullable=False, index=True)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False, index=True)

    client = db.relationship('Client', primaryjoin='ClientGroup.client_id == Client.id', backref='client_groups')
    group = db.relationship('AuthGroup', primaryjoin='ClientGroup.group_id == AuthGroup.id', backref='client_groups')



class ClientUserPermission(db.Model):
    __tablename__ = 'client_user_permissions'
    __table_args__ = (
        db.Index('client_user_permissions_client_id_permission_id_f418280d_uniq', 'client_id', 'permission_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.ForeignKey('client.id'), nullable=False, index=True)
    permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

    client = db.relationship('Client', primaryjoin='ClientUserPermission.client_id == Client.id', backref='client_user_permissions')
    permission = db.relationship('AuthPermission', primaryjoin='ClientUserPermission.permission_id == AuthPermission.id', backref='client_user_permissions')



class DjangoAdminLog(db.Model):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        db.CheckConstraint('"action_flag" >= 0)'),
    )

    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.DateTime, nullable=False)
    object_id = db.Column(db.Text)
    object_repr = db.Column(db.String(200), nullable=False)
    change_message = db.Column(db.Text, nullable=False)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id'), index=True)
    user_id = db.Column(db.ForeignKey('client.id'), nullable=False, index=True)
    action_flag = db.Column(db.Integer, nullable=False)

    content_type = db.relationship('DjangoContentType', primaryjoin='DjangoAdminLog.content_type_id == DjangoContentType.id', backref='django_admin_logs')
    user = db.relationship('Client', primaryjoin='DjangoAdminLog.user_id == Client.id', backref='django_admin_logs')



class DjangoContentType(db.Model):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        db.Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model'),
    )

    id = db.Column(db.Integer, primary_key=True)
    app_label = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)



class DjangoMigration(db.Model):
    __tablename__ = 'django_migrations'

    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    applied = db.Column(db.DateTime, nullable=False)



class DjangoSession(db.Model):
    __tablename__ = 'django_session'

    session_key = db.Column(db.String(40), primary_key=True)
    session_data = db.Column(db.Text, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False, index=True)



t_sqlite_sequence = db.Table(
    'sqlite_sequence',
    db.Column('name', db.NullType),
    db.Column('seq', db.NullType)
)
