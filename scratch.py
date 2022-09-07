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

unique_restaurants = list(set([d['restaurant'] for d in reviews]))

unique_restaurants_with_tag = []

for i in unique_restaurants:
    unique_restaurants_with_tag.append(list(
        filter(
            lambda rest: i in rest['name'], restaurants
        )
    )[0])

frontend = OrderedDict()

for categories in taxonomies:
    frontend[categories] = OrderedDict()
    for cat in taxonomies[categories]:
        frontend[categories][cat] = OrderedDict()
        for i in unique_restaurants_with_tag:
            restaurants_in_this_cat = list(filter(lambda rest: cat in rest['tags'], unique_restaurants_with_tag))
            for j in restaurants_in_this_cat:
                frontend[categories][cat][j['name']] = OrderedDict()
                frontend[categories][cat][j['name']] = list(filter(lambda rest: j['name'] in rest['restaurant'], reviews ))

pp.pprint(frontend)



