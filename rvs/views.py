import json
from flask import Blueprint, flash, render_template, request, session, escape, abort, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from models import User,Vlan,Switch,Cluster,Event,Iso,Node
from rvs import app
from rvs.models import db
from forms import LoginForm
from flask.ext.login import LoginManager

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
lm.session_protection = "strong"


@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

@app.route('/')
def index():
    return "Hello anonymous!"

@app.route('/desk')
@login_required
def desk():
    return render_template('desk.html',user=session['user_id']) 

@app.route('/api/users', methods = ['PUT'])
def update_user():
    if not (request.json or 'username' in request.json):
        return jsonify( {'result': False } ), 401

    user = User.query.filter_by(username=request.json['username']).first()
    db.session.add(user.from_json(request.get_json()))
    db.session.commit()
    return "OK", 201


@app.route('/api/users', methods = ['POST'])
def create_user():
    if not (request.json or request.json.viewkeys() & {'username', 'password'}):
        return jsonify( { 'result': False } ), 401

    user = User()
    db.session.add(user.from_json(request.get_json()))
    db.session.commit()
    return "OK", 201

@app.route('/api/users', methods = ['DELETE'])
def delete_user():
    if not (request.json or 'username' in request.json):
	return jsonify( {'result': False } ), 401

    user = User.query.filter_by(username=request.json['username']).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify( { 'result': True } ) 

@app.route('/api/users', methods = ['GET'])
@login_required
def get_users():
     cols = ['username', 'email', 'group', 'is_manager', 'managed_by']
     result = [{col: getattr(d, col) for col in cols} for d in User.query.all()]
     return jsonify( users = result  )

@app.route('/api/users/<user>', methods = ['GET'])
@login_required
def get_user(user):
     cols = ['username', 'email', 'group', 'is_manager', 'managed_by']
     result = [{col: getattr(d, col) for col in cols} for d in User.query.filter_by(username=user)]
     return jsonify( user = result )

@app.route('/desk/users')
@login_required
def Users():
     return render_template('users.html',data=User.query.all())


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
    
