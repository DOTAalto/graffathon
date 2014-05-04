# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.from_object('app.settings.common')
app.config.from_envvar('GRAFFATHON_SETTINGS')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

from models import SignUp, Admin
from forms import SignUpForm, LoginForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ilmoittautuminen', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	signups = SignUp.query.order_by(SignUp.created.desc())

	if request.method == 'POST' and form.validate_on_submit():
		signup = SignUp("", "", "", "")
		signup.name = form.name.data
		signup.email = form.email.data
		signup.school = form.school.data
		signup.experience = form.experience.data
		db.session.add(signup)
		db.session.commit()
		return redirect('/')

	return render_template('signup.html', form=form, signups=signups)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		login_user(form.admin)
		return redirect(request.args.get("next") or url_for('show_participants'))

	return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect('/')

@login_manager.user_loader
def load_user(userid):
	return Admin.query.get(int(userid))

@app.route('/osallistujat')
@login_required
def show_participants():
	signups = SignUp.query.order_by(SignUp.created.desc())
	return render_template('participants.html', signups=signups)