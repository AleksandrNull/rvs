import json
from flask import Blueprint, flash, render_template, request, session, escape, abort, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
import models

from models import User,Config,Vlan,Switch,Cluster,Event,Iso,Node
from rvs import app
from rvs.models import db
from forms import LoginForm
from flask.ext.login import LoginManager

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
lm.session_protection = "strong"

def get_handle(obj_name):
    allowed_dbs = [ "configs","users","clusters","nodes","vlans","switches","events","isos" ]

    if not obj_name in allowed_dbs:
        return jsonify( {'result': False } ), 401

    db_name=obj_name[:-1].title() if obj_name != "switches" else "Switch"
    model = getattr(models,db_name)
    try:
        cols = getattr(model,"allowed_fields")
    except:
        cols = model.__table__.c._data.keys() 

    if 'id' in cols: cols.remove('id')

    db_data = [ {"id":d.id, "values": { col: getattr(d, col) if col != 'password' else '*******' for col in cols}} for d in model.query.all() ]

    meta_res = [{"name": field, "datatype": model.__table__.c[field].info.split("#")[1], "label": model.__table__.c[field].info.split("#")[0], "editable": "True" } for field in cols if field != "password" ]

    if "password" in cols:
        meta_res += [{"name": "password", "datatype": "string", "label": "Password", "editable": "true" }]

    meta_res += [{"name": "action", "datatype": "html", "label": "", "editable": "false" }]    
  
    return jsonify( metadata = meta_res ,data = db_data )

@lm.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()

@app.route('/')
def index():
    return "Hello anonymous!"

@app.route('/desk')
@login_required
def desk():
    return render_template('desk.html',user=session['user_id']) 

@app.route('/api/users', methods = ['PUT'])
def update_user():
    if not (request.json and 'id' in request.json):
        return jsonify( {'result': False } ), 401
    user = User.query.filter_by(id=request.json['id']).first()
    if user is None:    
        return jsonify( {'result': False } ), 401
    user.from_json(request.get_json())
    db.session.add(user)
    db.session.commit()
    return jsonify( { 'result': True } )


@app.route('/api/users', methods = ['POST'])
def create_user():
    if not (request.json and request.json.viewkeys() & {'username', 'password'}):
        return jsonify( { 'result': False } ), 401

    user = User()
    db.session.add(user.from_json(request.get_json()))
    db.session.commit()
    return jsonify( { 'result': True } ) 

@app.route('/api/users', methods = ['DELETE'])
def delete_user():
    if not (request.json and 'id' in request.json):
        return jsonify( {'result': False } ), 401
    user = User.query.filter_by(id=request.json['id']).first()
    if user is None:
        return jsonify( {'result': False } ), 401

    db.session.delete(user)
    db.session.commit()
    return jsonify( { 'result': True } ) 

@app.route('/api/<obj>', methods = ['GET'])
@login_required
def get_obj(obj):
     return get_handle(obj)

@app.route('/api/users/<user>', methods = ['GET'])
@login_required
def get_user(user):
     cols = User.allowed_fields
     result = [{col: getattr(d, col) if col != 'password' else '*******' for col in cols} for d in User.query.filter_by(username=user)]
     return jsonify( user = result )

@app.route('/desk/<equip>')
@login_required
def Users(equip):
     return render_template('base.html',data=equip)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash("Logged in successfully.")
        session['user_id'] = form.user.username 
        return redirect(url_for("desk"))
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
