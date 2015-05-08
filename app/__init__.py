# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.contrib.fixers import ProxyFix

from datetime import datetime

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load configs
app.config.from_object('app.settings.common')
app.config.from_envvar('GRAFFATHON_SETTINGS')

@app.route('/')
def index():
    return render_template('index.html')
