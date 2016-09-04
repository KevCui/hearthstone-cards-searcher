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
        return str(target[attribute])
    else:
        return ''

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

# create rarities dict for rarity map
rarities = getOptionValue(soup.find('select', class_='rightselect'))
logging.debug('Rarities:\n' + str(rarities))

# fetch data from script and generate cards json
for script in soup.find_all('script'):
    if 'hearthstoneCards' in script.text:
        p = re.compile('var hearthstoneCards = \[{(.*?)\}]')
        raw = '[{' + p.search(script.text).group(1) + '}]'
        raw = raw.replace('popularity:', '"popularity":') # <- spent 1H to fix broken json! Dirty data...
        raw = raw.replace('[x]', '') # cleanup data
        logging.debug('--raw--')
        logging.debug(raw)

        rawjson = sorted(json.loads(raw), key=lambda k: int(k[sortby]), reverse=True)
        logging.debug('--json--')
        logging.debug(rawjson)

        break

# Prepared cards list for print
printCards = []
for card in rawjson:
    printCards.append([
        verifyValue(card, 'name'),
        verifyValue(card, 'cost'),
        verifyValue(card, 'attack'),
        verifyValue(card, 'health'),
        verifyValue(card, 'description'),
        sets[verifyValue(card, 'set')],
        races[verifyValue(card, 'race')],
        rarities[verifyValue(card, 'quality')], # why quality??
        verifyValue(card, 'popularity')
    ])
logging.debug(printCards)

# Print cards table
print(tabulate(printCards, ['Name', 'Cost', 'Attack', 'Life', 'Description', 'Set', 'Race', 'Rarity', 'Porularity'], tablefmt="grid"))
sys.exit(1)
