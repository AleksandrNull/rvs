from flask import Flask, render_template, request, session, escape, abort, redirect, url_for
from rvs import app, db, models


@app.route('/')
def index(name=None):
    if 'username' in session:
        return render_template('main.html',user=session['username']) 
    return redirect(url_for('login')) 

@app.route('/desk/<dept>')
def dept(dept):
    if 'username' in session:
        return render_template(dept+".html")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if valid_user(request.form['username'],request.form['password']):
        	session['username'] = request.form['username']
        	return redirect(url_for('index'))
        else:
            error = 'Invalid username/password'
    return render_template('login.html') 

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
    
def valid_user(user,passwd):
    if models.User.query.filter(models.User.name == user, models.User.passwd == passwd).count()==1:
    	return True
    return False

