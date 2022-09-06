import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])    

import_or_install('flask')
import_or_install('Frozen-Flask')
import_or_install('Flask-FlatPages')

import json
from flask import Flask, render_template
from flask_frozen import Freezer
from flask_flatpages import FlatPages
import sys


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

data = json.load(open('static/data.json', 'r'))

@app.route("/")
def home():
    context = {
        "title": "Hello Title",
        "description": "No you",
        "reviewers": data['reviewers']
    }
    return render_template( "home.jinja", **context )

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.debug = True
        app.run()
