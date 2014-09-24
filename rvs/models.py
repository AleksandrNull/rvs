from random import SystemRandom

from passlib.hash import sha256_crypt
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.sqlalchemy import SQLAlchemy
from rvs import app

db = SQLAlchemy(app)


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),info="Node name#string", unique=True)
    ipmi_ip = db.Column(db.String(12),info="IPMI IP#string", unique=False)
    ipmi_user = db.Column(db.String(30),info="IPMI user#string", unique=False)
    ipmi_pass = db.Column(db.String(30),info="IPMI password#string" , unique=False)
    port = db.Column(db.String(1000),info="Switches Ports#string", unique=True)
    enabled = db.Column(db.Boolean,info="Active#boolean", unique=False, default=True)
    cluster = db.Column(db.Integer,info="Cluster#integer", unique=False)

#    def __init__(self, name=None, ipmi_ip=None, ipmi_user=None, ipmi_pass=None, port=None, enabled=False, cluster=None):
#        self.name = name
#        self.ipmi_ip = ipmi_ip
#        self.ipmi_user = ipmi_user
#        self.ipmi_pass = ipmi_pass
#        self.port = port
#        self.enabled = enabled
#        self.cluster = cluster

    def __repr__(self):
        return '<Node %r>' % (self.name)

class Switch(db.Model):
    __tablename__ = 'switches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),info="Switch name#string", unique=True)
    mgmt_ip = db.Column(db.String(12),info="Switch management IP#string", unique=False)
    mgmt_user = db.Column(db.String(30),info="Mgmt User#string", unique=False)
    mgmt_pass = db.Column(db.String(30),info="Mgmt password#string", unique=False)
    mgmt_en_pass = db.Column(db.String(30), info="Mgmt EN password#string",unique=False)
    model = db.Column(db.String(30),info="Switch Model#string", unique=False)

#    def __init__(self, name=None, mgmt_ip=None, mgmt_user=None, mgmt_pass=None, mgmt_en_pass=None, model=None):
#        self.name = name
#        self.mgmt_ip = mgmt_ip
#        self.mgmt_user = mgmt_user
#        self.mgmt_pass = mgmt_pass
#        self.mgmt_en_pass = mgmt_en_pass
#        self.model = model

    def __repr__(self):
        return '<Switch %r>' % (self.name)

class Vlan(db.Model):
    __tablename__ = 'vlans'
    id = db.Column(db.Integer, primary_key=True)
    cluster = db.Column(db.Integer, info="Used in Cluster#integer", default=None)
    active = db.Column(db.Boolean, info="Active#boolean", default=True)
    reserved = db.Column(db.Boolean,info="Reserved#boolean", default=False)
#    desc = db.Column(db.String,info="Description#string")

#    def __init__(self, id=None, cluster=None, active=False, reserved=False):
#        self.id = id
#        self.cluster = cluster
#        self.active = active
#        self.reserved = reserved

    def __repr__(self):
        return 'Vlan %r>' % (self.id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),info="User name#string",unique=True)
    group = db.Column(db.String(50),info="User Group#string")
    _passwd = db.Column(db.LargeBinary(120))
    email = db.Column(db.String(120), info="E-mail#email",unique=True)
    is_manager = db.Column(db.Boolean, info="Manager#boolean",default=False)
    managed_by = db.Column(db.Integer, info="Under Management of#integer")
    allowed_fields = [ 'username', 'group', 'password', 'email', 'is_manager', 'managed_by' ]

    @hybrid_property
    def password(self):
        return self._passwd

    @password.setter
    def password(self, value):
        self._passwd = self._hash_password(value)

    def is_valid_password(self, password):
        return sha256_crypt.verify(password.encode("utf-8"), self._passwd)

    def _hash_password(self, password):
        return sha256_crypt.encrypt(password.encode("utf-8"))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def __repr__(self):
        return '<Uid#{:d}>'.format(self.id)

    def from_json(self,data):
        for f in self.allowed_fields:
            if f in data:
                setattr(self,f,data[f])
        return self

class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(2000), info="Description#string")
    owner = db.Column(db.Integer, info="Creator/Owner#integer")
    approved = db.Column(db.Boolean, info="Approved?#boolean", default=False)
    deleted = db.Column(db.Boolean, info="Deleted#boolean", default=False)
    status = db.Column(db.Integer, info="Current status#integer")
    vlans = db.Column(db.String(200),info="Used VLANs#string")
    config = db.Column(db.Integer, info="Deployment Config#integer")
    iso = db.Column(db.Integer, info="ISO used#integer")

#    def __init__(self, desc=None, owner=None, approved=False, deleted=False, status=None, vlans=None, config=None, iso=None):
#        self.desc = desc
#        self.owner = owner
#        self.approved = approved
#        self.deleted = deleted
#        self.status = status
#        self.vlans = vlans
#        self.config = config
#        self.iso = iso
 
    def __repr__(self):
        return '<Cluster %r>' % (self.id)

class Iso(db.Model):
    __tablename__ = 'isos'
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, info="Creator/Owner#integer")
    filename = db.Column(db.String(200),info="ISO Filename#string", unique=True)
    desc = db.Column(db.String(1000),info="ISO description#string")

#    def __init__(self, creator=None, filename=None, desc=None):
#        self.creator = creator
#        self.filename = filename
#        self.desc = desc
    
    def __repr__(self):
        return '<ISO %r>' % (self.filename)

class Config(db.Model):
    __tablename__ = 'configs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),info="Config name#string", unique=True)
    creator = db.Column(db.Integer,info="Creator/Owner#integer")
    data = db.Column(db.String(2000),info="Config#string")

    def __init__(self, name=None, creator=None, data=None):
        self.name = name
        self.creator = creator
        self.data = data

    def __repr__(self):
        return '<Config %r>' % (self.name)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, info="User#integer")
    action = db.Column(db.String(50), info="Action#string")
    cluster = db.Column(db.Integer, info="Cluster#integer")
    group = db.Column(db.Integer, info="Group#integer") # Probably need to remove
    switch = db.Column(db.Integer, info="Switch#integer")
    node = db.Column(db.Integer, info="Node#integer")
    iso = db.Column(db.Integer, info="ISO#integer")

#    def __init__(self, user=None, action=None, cluster=None, group=None, switch=None, node=None, iso=None ):
#        self.user = user
#        self.action = action
#        self.cluster = cluster
#        self.group = group
#        self.switch = switch
#        self.node = node
#        self.iso = iso

    def __repr__(self):
        return '<Action %r>' % (self.action)


