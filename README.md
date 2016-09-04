---
title: hsSearch
description: look up Hearthstone cards in terminal
author: KrazyCevin
tags: CLI, python, script
created:  04 Sep 2016
---

hsSearch
========
Show Hearthstone cards information in CLI. All cards data are collected from http://www.hearthhead.com/llected

### Requirement
* python3
* tabulate
* beautifulsoup4

### Install python package
* pip3 install -r requirements.txt

### How to use
```
usage: hsSearch.py [-h] [--standard] [--sort {cost,popularity}] [-a ATTACK]
                   [-l LIFE] [-cs COST]
                   [-r {dragon,mech,totem,demon,pirate,murloc,beast}]
                   [-rr {free,common,rare,epic,legendary}]
                   [-c {neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid}]
                   [-d]
                   [name [name ...]]

positional arguments:
  name                  search text

optional arguments:
  -h, --help            show this help message and exit
  --standard            standard cards only
  --sort {cost,popularity}
                        sort cards by cost or popularity. Default sort by cost
  -a ATTACK, --attack ATTACK
                        filter attack value
  -l LIFE, --life LIFE  filter life value
  -cs COST, --cost COST
                        filter mana cost
  -r {dragon,mech,totem,demon,pirate,murloc,beast}, --race {dragon,mech,totem,demon,pirate,murloc,beast}
                        filter race
  -rr {free,common,rare,epic,legendary}, --rarity {free,common,rare,epic,legendary}
                        filter by card rarity
  -c {neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid}, --class {neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid}
                        filter by class
  -d, --debug           active debug log
```

### Example
* List **Overload Epic** cards: ```hsSearch.py Overload -rr epic --standard```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/usage1.png "use case 1")

* List **0 cost Mage** card: ```hsSearch.py -cs 0 -c Mage```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/usage2.png "use case 2")

* List **12 Attack** point cards: ```hsSearch.py -a 12```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/usage3.png "use case 3")

* List **Medivh** card wiht **Neutral** class: ```hsSearch.py medivh -c neutral```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/usage4.png "use case 4")
