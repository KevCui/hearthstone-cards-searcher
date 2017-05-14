#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re, json
import logging
import urllib.request
import argparse

def configLog(debug):
    "Configure logging"
    logfile = os.path.basename(__file__).replace('.py', '.log') if debug == True else None
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
                if str(f) == 'text' and f.upper() not in str(card[f]).upper():
                    return True
                if str(f) != 'text' and str(card[f]).upper() not in [v.upper() for v in filter[f]]:
                    return True
            else:
                return True
    return False

def downloadImg(url, card):
    "Download card images from url to img"
    imgUrl      = url + card
    imgFolder   = os.path.dirname(__file__) + '/.img/'
    imgFullName = imgFolder + card

    logging.debug('Image Url: ' + imgUrl)

    if not os.path.exists(imgFolder):
        logging.debug('Creating img folder')
        os.makedirs(imgFolder)

    if not os.path.isfile(imgFullName):
        logging.debug('Downloading img: ' + card)
        urllib.request.urlretrieve(imgUrl, imgFullName)

def displayImg(cards):
    "Display img in terminal"
    imgPerRow = 10    # 8 card images per row
    imgWidth  = 150   # card image width 150px
    imgHeight = 225   # card image height 225px
    w3mimgdisplay = '/usr/lib/w3m/w3mimgdisplay'
    i = 0

    if os.path.isfile(w3mimgdisplay):
        for card in cards:
            imgFullName = os.path.dirname(__file__) + '/.img/' + card + '.png'
            try:
                x = ( i % imgPerRow) * imgWidth
                y = ( i // imgPerRow) * imgHeight
                logging.debug('Image: ' + str(i) + ' x: ' + str(x) + ' y: ' + str(y))

                os.system('echo -e "0;1;' + str(x) + ';' + str(y) + ';' + str(imgWidth) + ';' + str(imgHeight) + ';;;;;' + imgFullName + '\n4;\n3;" | ' + w3mimgdisplay)
                i += 1
            except:
                pass
    else:
        logging.debug('Not found ' + w3mimgdisplay)

def main():
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
    parser.add_argument('-m',  '--mana',   choices=['0','1','2','3','4','5','6','7','8','9','10','11','12','25'], default=['0','1','2','3','4','5','6','7','8','9','10','11','12','25'], nargs='*', help='filter mana')
    parser.add_argument('-f',  '--format', choices=['standard', 'wild'], default=['standard'], nargs='*', help='card set fromat: wild or standard')
    parser.add_argument('-s',  '--set',    choices=['basic', 'classic', 'kara', 'og', 'tgt', 'loe', 'brm', 'gvg', 'naxx', 'gadget', 'ungoro'], nargs='*', help='card set')
    parser.add_argument('-r',  '--race',   choices=['dragon', 'mech', 'totem', 'demon', 'pirate', 'murloc', 'beast', 'elemental'], nargs='*', help='filter race')
    parser.add_argument('-rr', '--rarity', choices=['free', 'common', 'rare', 'epic', 'legendary'], nargs='*', help='filter by card rarity')
    parser.add_argument('-c',  '--class',  choices=['neutral', 'warrior', 'priest',  'hunter', 'rogue', 'paladin', 'shaman', 'mage', 'warlock', 'druid'], dest='flclass', default='', nargs='*', help='filter by class')
    parser.add_argument('-i',  '--image',  action='store_true', dest="showimage", help='[Experimental] show card images using w3mimgdisplay')
    parser.add_argument('-d',  '--debug',  action='store_true', dest="debug", help='active debug log')

    args = parser.parse_args()
    if len(sys.argv) == 1 or (len(sys.argv) < 3 and args.debug != False):
        parser.print_help()
        sys.exit(1)

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
    printColWidth = [20, 4, 6, 6, 76, 6, 7, 7, 10, 10]

    paramDict = {
        'search' :     '%20'.join(args.name),
        'cost'   :     ','.join(args.mana),
        'type'   :     ','.join(args.type).upper(),
        'card_class':  ','.join(args.flclass).upper(),
        'format':      ','.join(args.format).upper() if len(args.format) < 2 else '',
        'collectible': 'true'
    }

    url = 'http://hearthstone.services.zam.com/v1/card?sort=cost,name'
    imgUrl = 'http://media.services.zam.com/v1/media/byName/hs/cards/enus/'

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
        'health': args.life,
        'cost'  : args.mana
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
    cardId = []
    for card in rawjson:
        if not isCardFilteredOut(card, filters):

            if args.showimage == True:
                downloadImg(imgUrl, card['card_id'] + '.png')

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
            cardId.append(card['card_id'])

    # Print cards table
    if len(printCards) == 1:
        print("Not match any Hearthstone cards.")
        sys.exit(1)

    table = texttable.Texttable()
    table.set_cols_width(printColWidth)
    table.add_rows(printCards)
    print(table.draw())

    # Show card images
    if args.showimage == True:
        displayImg(cardId)

if __name__ == '__main__':
    main()
