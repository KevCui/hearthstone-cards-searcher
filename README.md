---
title: hsSearch
description: look up Hearthstone cards in terminal
author: KrazyCevin
tags: CLI, python, script
created:  04 Sep 2016
---

hsSearch
========
Show Hearthstone cards information in CLI. All cards data are collected from http://www.hearthhead.com/

### Requirement
* Python3
* tabulate

### Install python package
* pip3 install tabulate

### How to use
```
usage: hsSearch.py [-h] [-a ATTACK] [-l LIFE] [-t TEXT] [-m MANA] [-tp TYPE]
                   [-s {basic,classic,kara,og,tgt,loe,brm}]
                   [-r {dragon,mech,totem,demon,pirate,murloc,beast}]
                   [-rr {free,common,rare,epic,legendary}]
                   [-c {neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid}]
                   [-d]
                   [name [name ...]]

positional arguments:
  name                  search text

optional arguments:
  -h, --help            show this help message and exit
  -a ATTACK, --attack ATTACK
                        filter attack value
  -l LIFE, --life LIFE  filter life value
  -t TEXT, --text TEXT  card description
  -m MANA, --mana MANA  filter mana
  -tp TYPE, --type TYPE
                        card type
  -s {basic,classic,kara,og,tgt,loe,brm}, --set {basic,classic,kara,og,tgt,loe,brm}
                        card set
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
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage1.png "use case 1")

* List **0 cost Mage** card: ```hsSearch.py -cs 0 -c Mage```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage2.png "use case 2")

* List **12 Attack** point cards: ```hsSearch.py -a 12```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage3.png "use case 3")

* List **Medivh** card wiht **Neutral** class: ```hsSearch.py medivh -c neutral```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage4.png "use case 4")
