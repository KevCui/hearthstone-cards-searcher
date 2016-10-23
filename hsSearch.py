#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re, json
import logging
import urllib.request
import argparse

def configLog(debug):
    "Configure logging"
    logfile = os.path.basename(__file__).replace('.py', '.log') if args.debug == True else None
    loglevel = logging.DEBUG if logfile is not None else None
    logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', filename=logfile, level=loglevel)

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
                if str(f) == 'text' and fv.upper() not in str(card[f]).upper():
                    return True
                if str(f) != 'text' and str(card[f]).upper() not in [v.upper() for v in filter[f]]:
                    return True
            else:
                return True
    return False

# Assert texttable is installed
try:
    import texttable
except ImportError:
    logging.critical("\nIt seems `texttable` is not installed. Please run pip install texttable")
    sys.exit(1)

# Setup parameter
#   run script with -d, active debug mode (log file will be created)
parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='*', help='search text')
parser.add_argument('-a',  '--attack', nargs='*', help='filter attack value')
parser.add_argument('-l',  '--life',   nargs='*', help='filter life value')
parser.add_argument('-t',  '--text',   nargs='*', help='card description')
parser.add_argument('-tp', '--type',   choices=['minon','spell','weapon'], default=['minion','spell','weapon'], nargs='*', help='card type')
parser.add_argument('-m',  '--mana',   choices=['0','1','2','3','4','5','6','7'], default=['0','1','2','3','4','5','6','7'], nargs='*', help='filter mana')
parser.add_argument('-f',  '--format', choices=['standard', 'wild'], default=['standard'], nargs='*', help='card set fromat: wild or standard')
parser.add_argument('-s',  '--set',    choices=['basic', 'classic', 'kara', 'og', 'tgt', 'loe', 'brm', 'gvg', 'naxx'], nargs='*', help='card set')
parser.add_argument('-r',  '--race',   choices=['dragon', 'mech', 'totem', 'demon', 'pirate', 'murloc', 'beast'], nargs='*', help='filter race')
parser.add_argument('-rr', '--rarity', choices=['free', 'common', 'rare', 'epic', 'legendary'], nargs='*', help='filter by card rarity')
parser.add_argument('-c',  '--class',  choices=['neutral', 'warrior', 'priest',  'hunter', 'rogue', 'paladin', 'shaman', 'mage', 'warlock', 'druid'], dest='flclass', default='', nargs='*', help='filter by class')
parser.add_argument('-d',  '--debug',  action='store_true', dest="debug", help='active debug log')
args = parser.parse_args()

# Config logging
configLog(args.debug)
logging.debug('args:\n' + str(args))

# Define variable
#   printCards: cards informations list for printing
#   printColWidth: columns width list
#   paramDict: dict for all params ued in url
#   url: search url
#   imgUrl: image url
printCards = [['Name', 'Cost', 'Attack', 'Life', 'Description', 'Type', 'Class', 'Set', 'Race', 'Rarity']]
printColWidth = [20, 4, 6, 6, 80, 6, 7, 7, 6, 10]

paramDict = {
    'search' :     '%20'.join(args.name),
    'cost'   :     ','.join(args.mana),
    'type'   :     ','.join(args.type).upper(),
    'card_class':  ','.join(args.flclass).upper(),
    'format':      ','.join(args.format).upper() if len(args.format) < 2 else '',
    'collectible': 'true'
}

url = 'http://hearthstone.services.zam.com/v1/card?sort=cost,name'
imgUrl = 'http://wow.zamimg.com/images/hearthstone/cards/enus/original/'

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
for card in rawjson:
    if not isCardFilteredOut(card, filters):
        printCards.append([
	    verifyValue(card, 'name'),
	    verifyValue(card, 'cost'),
	    verifyValue(card, 'attack'),
	    verifyValue(card, 'health'),
            verifyValue(card, 'text') + '\n' + imgUrl + card['card_id'] + '.png',
	    verifyValue(card, 'type'),
	    verifyValue(card, 'card_class'),
	    verifyValue(card, 'set'),
	    verifyValue(card, 'race'),
	    verifyValue(card, 'rarity')
	])

# Print cards table
if len(printCards) == 1:
    print("Not match any Hearthstone cards.")
    sys.exit(1)

table = texttable.Texttable()
table.set_cols_width(printColWidth)
table.add_rows(printCards)
print(table.draw())
