from random import SystemRandom

from backports.pbkdf2 import compare_digest,pbkdf2_hmac
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.sqlalchemy import SQLAlchemy
from rvs import app

db = SQLAlchemy(app)


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ipmi_ip = db.Column(db.String(12), unique=False)
    ipmi_user = db.Column(db.String(30), unique=False)
    ipmi_pass = db.Column(db.String(30), unique=False)
    port = db.Column(db.String(500), unique=True)
    enabled = db.Column(db.Boolean,unique=False, default=True)
    cluster = db.Column(db.Integer,unique=False)

    def __init__(self, name=None, ipmi_ip=None, ipmi_user=None, ipmi_pass=None, port=None, enabled=False, cluster=None):
        self.name = name
        self.ipmi_ip = ipmi_ip
        self.ipmi_user = ipmi_user
        self.ipmi_pass = ipmi_pass
        self.port = port
        self.enabled = enabled
        self.cluster = cluster

    def __repr__(self):
        return '<Node %r>' % (self.name)

class Switch(db.Model):
    __tablename__ = 'switches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    mgmt_ip = db.Column(db.String(12), unique=False)
    mgmt_user = db.Column(db.String(30), unique=False)
    mgmt_pass = db.Column(db.String(30), unique=False)
    mgmt_en_pass = db.Column(db.String(30), unique=False)
    model = db.Column(db.String(30), unique=False)

    def __init__(self, name=None, mgmt_ip=None, mgmt_user=None, mgmt_pass=None, mgmt_en_pass=None, model=None):
        self.name = name
        self.mgmt_ip = mgmt_ip
        self.mgmt_user = mgmt_user
        self.mgmt_pass = mgmt_pass
        self.mgmt_en_pass = mgmt_en_pass
        self.model = model

    def __repr__(self):
        return '<Switch %r>' % (self.name)

class Vlan(db.Model):
    __tablename__ = 'vlans'
    id = db.Column(db.Integer, primary_key=True)
    cluster = db.Column(db.Integer, unique=False)
    active = db.Column(db.Boolean,unique=False, default=True)
    reserved = db.Column(db.Boolean,unique=False, default=False)

    def __init__(self, id=None, cluster=None, active=False, reserved=False):
        self.id = id
        self.cluster = cluster
        self.active = active
        self.reserved = reserved

    def __repr__(self):
        return 'Vlan %r>' % (self.id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    group = db.Column(db.String(50))
    _passwd = db.Column(db.LargeBinary(120))
    _salt = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    is_manager = db.Column(db.Boolean, default=False)
    managed_by = db.Column(db.Integer)

    @hybrid_property
    def password(self):
        return self._passwd

    @password.setter
    def password(self, value):
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._passwd = self._hash_password(value)

    def is_valid_password(self, password):
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._passwd)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
        return bytes(buff)
   
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def __repr__(self):
        return '<Uid#{:d}>'.format(self.id)

class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(2000), unique=False)
    owner = db.Column(db.Integer, unique=False)
    approved = db.Column(db.Boolean, unique=False, default=False)
    deleted = db.Column(db.Boolean, unique=False, default=False)
    status = db.Column(db.Integer, unique=False)
    vlans = db.Column(db.String(200), unique=False)
    config = db.Column(db.Integer, unique=False)
    iso = db.Column(db.Integer, unique=False)

    def __init__(self, desc=None, owner=None, approved=False, deleted=False, status=None, vlans=None, config=None, iso=None):
        self.desc = desc
        self.owner = owner
        self.approved = approved
        self.deleted = deleted
        self.status = status
        self.vlans = vlans
        self.config = config
        self.iso = iso
 
    def __repr__(self):
        return '<Cluster %r>' % (self.id)

class Iso(db.Model):
    __tablename__ = 'isos'
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, unique=False)
    filename = db.Column(db.String(200), unique=True)
    desc = db.Column(db.String(1000),unique=False)

    def __init__(self, creator=None, filename=None, desc=None):
        self.creator = creator
        self.filename = filename
        self.desc = desc
    
    def __repr__(self):
        return '<ISO %r>' % (self.filename)

class Config(db.Model):
    __tablename__ = 'configs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    creator = db.Column(db.Integer, unique=False)
    data = db.Column(db.String(2000),unique=False)

    def __init__(self, name=None, creator=None, date=None):
	self.name = name
	self.creator = creator
        self.data = data

    def __repr__(self):
        return '<Config %r>' % (self.name)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, unique=False)
    action = db.Column(db.String(50), unique=False)
    cluster = db.Column(db.Integer, unique=False)
    group = db.Column(db.Integer, unique=False)
    switch = db.Column(db.Integer, unique=False)
    node = db.Column(db.Integer, unique=False)
    iso = db.Column(db.Integer, unique=False)

    def __init__(self, user=None, action=None, cluster=None, group=None, switch=None, node=None, iso=None ):
        self.user = user
        self.action = action
        self.cluster = cluster
        self.group = group
        self.switch = switch
        self.node = node
        self.iso = iso

    def __repr__(self):
        return '<Action %r>' % (self.action)


