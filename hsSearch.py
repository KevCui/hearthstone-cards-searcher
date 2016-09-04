#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, json
import logging
import urllib.request
import argparse

def getOptionValue(soup):
    "return list of option value: option text"
    tmp = {}
    for opt in soup.find_all('option'):
        try:
            tmp[opt['value']] = opt.string
        except:
            pass
    tmp[''] = '' # add defaut empty value
    return tmp

def verifyValue(target, attribute):
    "verify attribute exists in target"
    if attribute in target.keys():
        if attribute == "set":
            logging.debug(target)
        return str(target[attribute])
    else:
        return ''

def isCardFiltered(card, filter):
    "filter card by filters"
    if filter:
        for f in filter:
            if f in card.keys():
                if str(card[f]) != str(filter[f]):
                    return True
            else:
                return True
    return False

def setNoneValue(data, filter):
    "set None value in data ilterif it doesn't exist according to filter list"
    tmp = []
    for card in data:
        for f in filter:
            if f not in card.keys():
                card[f] = ''
        tmp.append(card)
    return tmp

# Assert beautifulsoup is installed
try:
    from bs4 import BeautifulSoup
except ImportError:
    log.critical("It seems `beautifulsoup` is not installed. Please run pip install -r requirements.txt")
    sys.exit(1)

# Assert tabulate is installed
try:
    from tabulate import tabulate
except ImportError:
    log.critical("It seems `tabulate` is not installed. Please run pip install -r requirements.txt")
    sys.exit(1)

# Setup parameter
#   run script with -s, set sortby value
#   run script with -d, active debug mode (log file will be created)
parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='*', help='search text')
parser.add_argument('-s', '--sort', choices=['cost', 'popularity'], dest="sortby", help='sort cards by cost or popularity. Default sort by cost')
parser.add_argument('-a', '--attack', help='filter attack value')
parser.add_argument('-l', '--life', help='filter life value')
parser.add_argument('-cs', '--cost', help='filter mana cost')
parser.add_argument('-r', '--race', choices=['', 'dragon', 'mech', 'totem', 'demon', 'pirate', 'murloc', 'beast'], help='filter race')
parser.add_argument('-c', '--class', choices=['neutral', 'warrior', 'priest',  'hunter', 'rogue', 'paladin', 'shaman', 'mage', 'warlock', 'druid'], dest='flclass', help='filter by class')
parser.add_argument('-d', '--debug',  action='store_true', dest="debug", help='active debug log')
args = parser.parse_args()

# Config logging
logfile = 'hssearch.log' if args.debug == True else None
loglevel = logging.DEBUG if logfile is not None else None
logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', filename=logfile, level=loglevel)
logging.debug('args:\n' + str(args))

# Define variable
#   rootUrl: hearthhead.com:
#   url: search url
rootUrl = 'http://www.hearthhead.com/cards=?filter=na='
url = rootUrl + '+'.join(args.name) + ';ex=on#text'
logging.debug('\n' + url)
#   sortby: sortby value if it exits
sortby = "cost" if args.sortby is None else args.sortby
logging.debug('sortby: ' + sortby)

# create classes dict for class map
classes = {
    '':     'Neutral',
    '1':    'Warrior',
    '2':    'Priest',
    '3':    'Hunter',
    '4':    'Rogue',
    '5':    'Paladin',
    '7':    'Shaman',
    '8':    'Mage',
    '9':    'Warlock',
    '11':   'Druid'
}

# create http request
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
soup = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")

# create races dict for race map
# create sets dict for set pack map
for filter in soup.find('table', class_='filter-table').find_all('tr'):
    if 'Race:' in filter.get_text():
        races = getOptionValue(filter)
        logging.debug('Races:\n' + str(races))

    if 'Set:' in filter.get_text():
        sets = getOptionValue(filter)
        logging.debug('Sets:\n' + str(sets))

# create rarities dict for quality map
rarities = getOptionValue(soup.find('select', class_='rightselect'))
logging.debug('Rarities:\n' + str(rarities))

# create filters
filters = {}
if args.flclass is not None:
    filters['classs'] = list(classes.keys())[list(classes.values()).index(args.flclass[0].upper() + args.flclass[1:])]
if args.race is not None:
    filters['race'] = list(races.keys())[int(list(races.values()).index(args.race[0].upper() + args.race[1:]))]
if args.attack is not None:
    filters['attack'] = args.attack
if args.life is not None:
    filters['health'] = args.life
if args.cost is not None:
    filters['cost'] = args.cost
logging.debug('Filters:\n' + str(filters))

# fetch data from script and generate cards json
for script in soup.find_all('script'):
    if 'hearthstoneCards' in script.text:
        p = re.compile('var hearthstoneCards = \[{(.*?)\}]')
        raw = '[{' + p.search(script.text).group(1) + '}]'
        raw = raw.replace('popularity:', '"popularity":') # <- spent 1H to fix broken json! Dirty data...
        raw = raw.replace('[x]', '') # cleanup data
        logging.debug('--raw--')
        logging.debug(raw)

        rawjson= sorted(json.loads(raw), key=lambda k: int(k[sortby]), reverse=True)
        logging.debug('--json--')
        logging.debug(rawjson)
        rawlist = setNoneValue(rawjson, filters)
        logging.debug('--list--')
        logging.debug(rawjson)

        break
try:
    rawjson
except NameError:
    print("Not match any Hearthstone cards.")
    sys.exit(1)

# Prepared cards list for print
printCards = []
for card in rawjson:
    try:
        if not isCardFiltered(card, filters):
            printCards.append([
                verifyValue(card, 'name'),
                verifyValue(card, 'cost'),
                verifyValue(card, 'attack'),
                verifyValue(card, 'health'),
                verifyValue(card, 'description'),
                classes[verifyValue(card, 'classs')], # why classs??
                sets[verifyValue(card, 'set')],
                races[verifyValue(card, 'race')],
                rarities[verifyValue(card, 'quality')], # why quality??
                verifyValue(card, 'popularity')
            ])
    except:
        pass
logging.debug(printCards)

# Print cards table
#   printTitle: print table head title
printTitle = ['Name', 'Cost', 'Attack', 'Life', 'Description', 'Class', 'Set', 'Race', 'Rarity', 'Porularity']
print(tabulate(printCards, printTitle, tablefmt="grid"))
