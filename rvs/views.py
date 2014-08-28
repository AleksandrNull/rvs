from flask import Blueprint, flash, render_template, request, session, escape, abort, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from models import User,Vlan,Switch,Cluster,Event,Iso,Node
from rvs import app
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

@app.route('/api/users', methods = ['GET'])
@login_required
def get_users():
     return jsonify(json_list = User.query.all())

@app.route('/api/users/<user>', methods = ['GET'])
@login_required
def get_user():
     return jsonify(json_list = User.query.filter_by(username=user))


@app.route('/desk/users')
@login_required
def Users():
     return render_template('users.html',data=User.query.all())


#@app.route('/desk/<dept>')
#@login_required
#def dept(dept):
#    datapost = 
#    return render_template(dept+".html")

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
    
