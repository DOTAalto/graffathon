# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user, logout_user
from flask.ext.mail import Message, Mail
from flask.ext.thumbnails import Thumbnail

from flask_errormail import mail_on_500
from datetime import datetime

from os import listdir
from os.path import isfile, join


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load configs
app.config.from_object('app.settings.common')
app.config.from_envvar('GRAFFATHON_SETTINGS')

mail_on_500(app, app.config['ADMINISTRATORS'],
            sender=app.config['MAIL_DEFAULT_SENDER'])

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

mail = Mail(app)
mail.init_app(app)

thumb = Thumbnail(app)

from models import SignUp, Admin
from forms import SignUpForm, LoginForm
from emails import send_email, send_all


# TODO: handling all these static page routes
# manually is stupid. generate url's automatically
# by walking the template directory and doing conversion
# (_ -> -,) for urls and / -> _ for function names.
# eg. /info/test-page -> template: info/test_page.html,
# function name: info_test_page (usable for menus)

@app.route('/')
def index():
    return render_template('index.html')

# In development, serve media using flask.
@app.route('/media/<path:filename>')
def download_file(filename):
    if app.config['DEBUG']:
        return send_from_directory(app.config['MEDIA_FOLDER'],
                                   filename)

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


@app.route('/osallistujat', methods=['GET', 'POST'])
@login_required
def show_participants():
    if request.method == 'POST':
        if request.form['button'] == 'Maksanut':
            participant_ids = request.form.getlist("selected_paid")
            p_list = SignUp.query.filter(SignUp.id.in_(participant_ids))

            messages = []
            mail_subject = "Graffathon – Maksu vahvistettu"

            for p in p_list:
                p.paid = True
                mail_body = render_template("mails/payment_received.txt",
                                            participant=p)
                messages.append(Message(recipients=[p.email],
                                        body=mail_body,
                                        subject=mail_subject))

            send_all(messages)
            db.session.commit()

            return redirect(url_for('show_participants'))

        elif request.form['button'] == 'Poista':
            participant_ids = request.form.getlist("selected_remove")
            p_list = SignUp.query.filter(SignUp.id.in_(participant_ids))

            mail_subject = "Graffathon - Ilmoittautumisesi on poistettu"
            messages = []

            for p in p_list:
                p.visible = False
                mail_body = render_template("mails/signup_removed.txt",
                                            participant=p)
                messages.append(Message(recipients=[p.email],
                                        body=mail_body,
                                        subject=mail_subject))

            send_all(messages)
            db.session.commit()

            return redirect(url_for('show_participants'))

        elif request.form['button'] == 'Vahvista':
            participant_ids = request.form.getlist("selected_confirmation")
            p_list = SignUp.query.filter(SignUp.id.in_(participant_ids))

            messages = []
            mail_subject = "Graffathon - Maksutiedot"

            # Create one mail message for every participant
            # and send them over single connection
            for p in p_list:
                p.confirmed = True
                p.confirmed_at = datetime.utcnow()
                mail_body = render_template("mails/payment_info_cash.txt",
                                            participant=p)
                messages.append(Message(recipients=[p.email],
                                        body=mail_body,
                                        subject=mail_subject))

            send_all(messages)
            db.session.commit()

            return redirect(url_for('show_participants'))

        elif request.form['button'] == 'Poista ilmoittautuminen':
            participant_ids = request.form.getlist("confirmation_remove")
            p_list = SignUp.query.filter(SignUp.id.in_(participant_ids))

            for p in p_list:
                p.visible = False
            db.session.commit()

            return redirect(url_for('show_participants'))

        elif request.form['button'] == 'Muistuta':
            participant_ids = request.form.getlist("selected_reminder")
            p_list = SignUp.query.filter(SignUp.id.in_(participant_ids))

            messages = []
            mail_subject = "Graffathon - Muistutus"

            # Create one mail message for every participant
            # and sen them over single connection

            for p in p_list:
                mail_body = render_template("mails/payment_late.txt",
                                            participant=p)
                messages.append(Message(recipients=[p.email],
                                        body=mail_body,
                                        subject=mail_subject))

            send_all(messages)

            # Flash a message for the admin.
            flash(u'Muistutus lähetetty')


    signups = SignUp.query.filter_by(confirmed=True, visible=True).order_by(SignUp.created.asc())
    confirmation = SignUp.query.filter_by(confirmed=False, visible=True).order_by(SignUp.created.asc())
    hidden_participants = SignUp.query.filter_by(visible=False)
    return render_template('participants.html',
                           signups=signups,
                           confirmation=confirmation,
                           hidden_participants=hidden_participants)
