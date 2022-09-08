import pip
import os


# This is for cloudflare pages ---------
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])    


if not os.environ['USER'] == 'suhail':
    import_or_install('flask')
    import_or_install('Frozen-Flask')
    import_or_install('Flask-FlatPages')
# --------------------------------------

import json
from flask import Flask, render_template
from flask_frozen import Freezer
from flask_flatpages import FlatPages
from collections import OrderedDict
import sys

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

data = json.load(open('static/data.json', 'r'), object_pairs_hook=OrderedDict)

def get_formatted_data():
    taxonomies = data['taxonomies']
    reviews = data['reviews']
    bios = data['reviewers']
    restaurants = data['restaurants']

    for i in reviews:
        i['photo'] = list(
            filter(
                lambda person: person['name'] == i['reviewer'], bios)
        )[0]['photo']
        i['tags'] = list(
            filter(
                lambda restaurant: restaurant['name'] == i['restaurant'], restaurants)
        )[0]['tags']

    unique_restaurants = list(set([d['restaurant'] for d in reviews]))

    unique_restaurants_with_tag = []

    for i in unique_restaurants:
        unique_restaurants_with_tag.append(list(
            filter(
                lambda rest: i in rest['name'], restaurants
            )
        )[0])

    frontend = OrderedDict()

    # I forgot what's going on here or why I did this
    for categories in taxonomies:
        frontend[categories] = OrderedDict()
        for cat in taxonomies[categories]:
            frontend[categories][cat] = OrderedDict()
            for i in unique_restaurants_with_tag:
                restaurants_in_this_cat = list(filter(lambda rest: cat in rest['tags'], unique_restaurants_with_tag))
                for j in restaurants_in_this_cat:
                    frontend[categories][cat][j['name']] = OrderedDict()
                    frontend[categories][cat][j['name']] = list(
                        filter(lambda rest: j['name'] in rest['restaurant'], reviews))

    return frontend


@app.route("/")
def home():
    context = {
        "title": "Food, we need food!",
        "reviewers": data['reviewers'],
        "big_data": get_formatted_data()
    }
    return render_template( "home.jinja", **context )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.debug = True
        app.run()
