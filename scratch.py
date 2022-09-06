import json
from collections import OrderedDict
import pprint

pp = pprint.PrettyPrinter(indent=2)

data = json.load(open('static/data.json', 'r'), object_pairs_hook=OrderedDict)

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


frontend = OrderedDict()

for categories in taxonomies:
    frontend[categories] = OrderedDict()
    for cat in taxonomies[categories]:
        frontend[categories][cat] = list(
            filter(
                lambda rest: cat in rest['tags'], reviews
            )
        )

# pp.pprint(reviews)
pp.pprint(frontend)
