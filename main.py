from datetime import datetime

import json
from flask import Flask, render_template
from flask_frozen import Freezer
from flask_flatpages import FlatPages
from collections import OrderedDict
import pprint 
import sys




app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

data = json.load(open('static/data.json', 'r'), object_pairs_hook=OrderedDict)
pp = pprint.PrettyPrinter(indent=4)

taxonomies = data['taxonomies']
reviews = data['reviews']
bios = data['reviewers']
restaurants = data['restaurants']

@app.template_filter()
def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%b, %Y')

@app.template_filter('prettyprint')
def prettyprint_filter(value):
    return json.dumps(value, indent=4)

def get_address_from_name(name):
    for i in restaurants:
        if i['name'] == name:
            if 'address' in i:
                return i['address']
    return False

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
        try:
            i['tags'] = list(
                filter(
                    lambda restaurant: restaurant['name'] == i['restaurant'], restaurants)
            )[0]['tags']
        except:
            print('No tags in ', i)

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
                    frontend[categories][cat][j['name']] = {}
                    if get_address_from_name(j['name']):
                        frontend[categories][cat][j['name']]['address'] = get_address_from_name(j['name'])
                    frontend[categories][cat][j['name']]['comments'] = len(list(
                        filter(lambda rest: j['name'] in rest['restaurant'], reviews)))
                    frontend[categories][cat][j['name']]['reviews'] = list(
                        filter(lambda rest: j['name'] in rest['restaurant'], reviews))

    return frontend


def get_profile_reviews(username):
    joined = []
    filtered_reviews = list(filter(lambda review: username in review['reviewer'], reviews))
    for rev in filtered_reviews:
        rev['tags'] = list(filter(lambda rest: rest['name']  in rev['restaurant'], restaurants))[0]['tags']

    return filtered_reviews

@app.route("/")
def home():
    context = {
        "title": "Food, we need food!",
        "reviewers": data['reviewers'],
        "big_data": get_formatted_data(),
        "last_updated": datetime.utcnow().strftime('%b %-d, %Y'),
    }
    return render_template( "home.jinja", **context )

@app.route("/<username>/", methods=['GET'], strict_slashes=False)
def profile(username):

    filtered = []
    formatted = get_formatted_data()

    for i in formatted:
        for j in formatted[i]:
            for k in formatted[i][j]:
                for l in formatted[i][j][k]['reviews']:
                    if username == l['reviewer']:
                        filtered.append(formatted[i][j][k])

    de_dup = []
    for f in filtered:
        f['restaurant'] = f['reviews'][0]['restaurant']
    
    for f in filtered:
        if len((list(filter(lambda hola:hola['restaurant'] == f['restaurant'], de_dup)))) > 0:
            print("Duplicate", f['restaurant'])
        else:
            de_dup.append(f)

    context = {
        "title": f'Recommendations by {username}',
        "profile": list(filter(lambda person: person['name'] == username, bios))[0],
        "big_data": de_dup
    }
    return render_template( "profile.jinja", **context )

@freezer.register_generator
def profile():
    for i in bios:
        yield {
            'username': i['name']
         }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.debug = True
        app.run()
