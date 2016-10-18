#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, json
import logging
import urllib.request
import argparse

def verifyValue(target, attribute):
    "Verify attribute exists in target"
    if attribute in target.keys():
        return str(target[attribute]).replace('<b>', '').replace('</b>', '').replace('\n', '')
    else:
        return ''

def isCardFilteredOut(card, filter):
    "Filter card by filters"
    if filter:
        for f in filter:
            if f in card.keys():
                if str(f) == 'text' and str(filter[f]).upper() not in str(card[f]).upper():
                    return True
                if str(f) != 'text' and str(filter[f]).upper() != str(card[f]).upper():
                    return True
            else:
                return True
    return False

# Assert tabulate is installed
try:
    from tabulate import tabulate
except ImportError:
    logging.critical("\nIt seems `tabulate` is not installed. Please run pip install -r requirements.txt")
    sys.exit(1)

# Setup parameter
#   run script with -s, set sortby value
#   run script with -d, active debug mode (log file will be created)
parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='*', help='search text')
parser.add_argument('-a',  '--attack', help='filter attack value')
parser.add_argument('-l',  '--life',   help='filter life value')
parser.add_argument('-t',  '--text',   help='card description')
parser.add_argument('-m',  '--mana',   default='0,1,2,3,4,5,6,7', help='filter mana')
parser.add_argument('-tp', '--type',   default='minion,spell,weapon', help='card type')
parser.add_argument('-s',  '--set',    choices=['basic', 'classic', 'kara', 'og', 'tgt', 'loe', 'brm'], help='card set')
parser.add_argument('-r',  '--race',   choices=['dragon', 'mech', 'totem', 'demon', 'pirate', 'murloc', 'beast'], help='filter race')
parser.add_argument('-rr', '--rarity', choices=['free', 'common', 'rare', 'epic', 'legendary'], help='filter by card rarity')
parser.add_argument('-c',  '--class',  choices=['neutral', 'warrior', 'priest',  'hunter', 'rogue', 'paladin', 'shaman', 'mage', 'warlock', 'druid'], dest='flclass', default='', help='filter by class')
parser.add_argument('-d',  '--debug',  action='store_true', dest="debug", help='active debug log')
args = parser.parse_args()

# Config logging
logfile = 'hssearch.log' if args.debug == True else None
loglevel = logging.DEBUG if logfile is not None else None
logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', filename=logfile, level=loglevel)
logging.debug('args:\n' + str(args))

# Define variable
#   paramDict: dict for all params ued in url
#   url: search url
paramDict = {
    'search' : '%20'.join(args.name),
    'cost' : args.mana,
    'type' : str(args.type).upper(),
    'card_class': str(args.flclass).upper(),
    'format': 'STANDARD',
    'collectible': 'true'
}

url = 'http://hearthstone.services.zam.com/v1/card?sort=cost,name'
for k in paramDict:
    if paramDict[k]:
        url += '&' + str(k) + '=' + str(paramDict[k])
logging.debug('url: ' + url)

# Create filters
#   filters: dict for filters
filters = {
    'set'   : args.set,
    'text'  : args.text,
    'race'  : args.race,
    'rarity': args.rarity,
    'attack': args.attack,
    'health': args.life
}

#   remove None value filter item
filters = dict((k, v) for k, v in filters.items() if v)
logging.debug('Filters:\n' + str(filters))

# Create http request
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
rawjson = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
logging.debug('json:\n' + str(rawjson))

# Prepare cards list for print
printCards = []
for card in rawjson:
    if not isCardFilteredOut(card, filters):
        printCards.append([
	    verifyValue(card, 'name'),
	    verifyValue(card, 'cost'),
	    verifyValue(card, 'attack'),
	    verifyValue(card, 'health'),
	    verifyValue(card, 'text'),
	    verifyValue(card, 'type'),
	    verifyValue(card, 'card_class'),
	    verifyValue(card, 'set'),
	    verifyValue(card, 'race'),
	    verifyValue(card, 'rarity')
	])

# Print cards table
#   printTitle: print table head title
if len(printCards) == 0:
    print("Not match any Hearthstone cards.")
    sys.exit(1)

printTitle = ['Name', 'Cost', 'Attack', 'Life', 'Description', 'Type', 'Class', 'Set', 'Race', 'Rarity']
print(tabulate(printCards, printTitle, tablefmt="grid"))
