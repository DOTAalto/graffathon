# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.contrib.fixers import ProxyFix

from datetime import datetime

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load configs
app.config.from_object('app.settings.common')
app.config.from_envvar('GRAFFATHON_SETTINGS')

RESULTS = [
  [1,215,u'Moonwalk - JET~TAP'],
  [2,211,u'get rekt - FruitieX, remedi, atte'],
  [3,188,u'GeomeX - Parallel Places'],
  [4,175,u't-rekt - t-rekt'],
  [5,170,u'Zef - Gluster'],
  [6,162,u'CubeProcess - BJAKKE'],
  [7,160,u'Summer Cartridge - Toivo Järvi and Erik Pekkarinen'],
  [8,151,u'To be anounced - In4K'],
  [9,151,u'Kiitos Ämpäri - Saksalainen Laatu'],
  [10,144,u'Odyssey - Skeletor'],
  [11,138,u'Flying with no wings - Bansku'],
  [12,127,u'The All-Seeing - Jupp3'],
  [13,124,u'colorful cubes in a grayscale world - Walther, Korkkii'],
  [14,124,u'I Want To Evolve - Primitive'],
  [15,122,u'Randomitology - KLH'],
  [16,121,u'summer time blues - Rakshith , Raghavendra, Suhas'],
  [17,117,u'Fruits - Karate Ink Sirup'],
  [18,117,u'NATIIVIA.EXE - Team dagenEfter'],
  [19,115,u'Polyheadache - Team MiViWi'],
  [20,113,u'Spooky - Crabhics'],
  [21,107,u'Rainbow mix - Martin Radev'],
  [22,103,u'No Home - voi-pojat'],
  [23,101,u'Control - ineiros'],
  [24,96,u'Red - Hemaolle'],
  [25,95,u'valtakunta - horror terror elite legion'],
  [26,91,u'dat bass - Scho-ka-kola'],
  [27,82,u'WorkInProgress - Xywzel'],
  [28,82,u'play for freedom - Yao Lu & Julian Kołłątaj'],
  [29,78,u'Derp - Keksinimi'],
  [30,76,u'3d fire disco - Adarsh Krishnan'],
  [31,74,u'Sähköjänis - JuMiPallot'],
  [32,64,u'DX9 4k Framework - @RemesJann'],
]
LINKS = [
    "https://www.youtube.com/watch?v=XEAE0FyNERA&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=1",
    "https://www.youtube.com/watch?v=pWyp6SAllY4&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=2",
    "https://www.youtube.com/watch?v=InN-bmRk2lQ&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=3",
    "https://www.youtube.com/watch?v=bYpXWAsFYvM&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=4",
    "https://www.youtube.com/watch?v=XucfklQa6iA&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=5",
    "https://www.youtube.com/watch?v=UC-lTdqXrh4&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=6",
    "https://www.youtube.com/watch?v=O7qWdIpcNTs&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=7",
    "https://www.youtube.com/watch?v=1ctdbP-ySWI&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=8",
    "https://www.youtube.com/watch?v=4GQ2yo7KkEs&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=9",
    "https://www.youtube.com/watch?v=7Jq9b5nVhe4&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=10",
    "https://www.youtube.com/watch?v=maNziCIArqI&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=11",
    "https://www.youtube.com/watch?v=MSX29PxaYAg&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=12",
    "https://www.youtube.com/watch?v=-kLHD0Qjih4&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=13",
    "https://www.youtube.com/watch?v=tD5XEAXU_jg&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=14",
    "https://www.youtube.com/watch?v=ERxSwJPgitA&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=15",
    "https://www.youtube.com/watch?v=OAPMYZS1PyQ&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=16",
    "https://www.youtube.com/watch?v=T4cf_aLv0MA&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=17",
    "https://www.youtube.com/watch?v=NyYf9rWSRSs&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=18",
    "https://www.youtube.com/watch?v=qXLMylnUWY8&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=19",
    "https://www.youtube.com/watch?v=UjBqglMQDM4&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=20",
    "https://www.youtube.com/watch?v=iM-Gvwpwufg&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=21",
    "https://www.youtube.com/watch?v=NQ-5HE_KWwQ&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=22",
    "https://www.youtube.com/watch?v=xV_89Lz2qxs&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=23",
    "https://www.youtube.com/watch?v=1vZ31315nms&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=24",
    "https://www.youtube.com/watch?v=tnclamheH4c&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=25",
    "https://www.youtube.com/watch?v=1PZ2GUWwd78&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=26",
    "https://www.youtube.com/watch?v=OEf9vGoKnVQ&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=28",
    "https://www.youtube.com/watch?v=neyRa6Fmap4&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=27",
    "https://www.youtube.com/watch?v=4ZMmIqcHM54&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=29",
    "https://www.youtube.com/watch?v=8W6zrTQ-Fkw&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=30",
    "https://www.youtube.com/watch?v=hdu9tcCcrq0&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=31",
    "https://www.youtube.com/watch?v=Or-fInNS4XE&list=PLmRDkQf8W1WFboD7M9xoLUf_pRwz6kL9c&index=32"
]

@app.route('/')
def index():
    return render_template('index.html', results=RESULTS, links=LINKS)

@app.route('/archive')
def archive():
    return redirect('/2014/archive.html')
