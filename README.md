---
Title: hsSearcher
Description: look up Hearthstone cards in terminal
Author: KrazyCavin
Tags: CLI, python, script
created:  04 Sep 2016
---

hsSearcher [RIP]
==========

# Due to the server close, this script is not working :(

Show Hearthstone cards information in CLI. All cards data are collected from http://www.hearthhead.com/

### Requirement
* Python3
* texttable

### Install python package
* pip install texttable

### How to use
```
usage: hsSearch.py [-h] [-a [ATTACK [ATTACK ...]]] [-l [LIFE [LIFE ...]]]
                   [-t [TEXT [TEXT ...]]]
                   [-tp [{minon,spell,weapon,hero} [{minon,spell,weapon,hero} ...]]]
                   [-m [{0,1,2,3,4,5,6,7,8,9,10,11,12,25} [{0,1,2,3,4,5,6,7,8,9,10,11,12,25} ...]]]
                   [-f [{standard,wild} [{standard,wild} ...]]]
                   [-s [{basic,classic,kara,og,tgt,loe,brm,gvg,naxx,gadget,ungoro,icecrown,lootapalooza,gilneas,boomsday} [{basic,classic,kara,og,tgt,loe,brm,gvg,naxx,gadget,ungoro,icecrown,lootapalooza,gilneas,boomsday} ...]]]
                   [-r [{dragon,mech,totem,demon,pirate,murloc,beast,elemental} [{dragon,mech,totem,demon,pirate,murloc,beast,elemental} ...]]]
                   [-rr [{free,common,rare,epic,legendary} [{free,common,rare,epic,legendary} ...]]]
                   [-c [{neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid} [{neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid} ...]]]
                   [-i] [-d]
                   [name [name ...]]

positional arguments:
  name                  search text

optional arguments:
  -h, --help            show this help message and exit
  -a [ATTACK [ATTACK ...]], --attack [ATTACK [ATTACK ...]]
                        filter attack value
  -l [LIFE [LIFE ...]], --life [LIFE [LIFE ...]]
                        filter life value
  -t [TEXT [TEXT ...]], --text [TEXT [TEXT ...]]
                        card description
  -tp [{minon,spell,weapon,hero} [{minon,spell,weapon,hero} ...]], --type [{minon,spell,weapon,hero} [{minon,spell,weapon,hero} ...]]
                        card type
  -m [{0,1,2,3,4,5,6,7,8,9,10,11,12,25} [{0,1,2,3,4,5,6,7,8,9,10,11,12,25} ...]], --mana [{0,1,2,3,4,5,6,7,8,9,10,11,12,25} [{0,1,2,3,4,5,6,7,8,9,10,11,12,25} ...]]
                        filter mana
  -f [{standard,wild} [{standard,wild} ...]], --format [{standard,wild} [{standard,wild} ...]]
                        card set fromat: wild or standard
  -s [{basic,classic,kara,og,tgt,loe,brm,gvg,naxx,gadget,ungoro,icecrown,lootapalooza,gilneas,boomsday} [{basic,classic,kara,og,tgt,loe,brm,gvg,naxx,gadget,ungoro,icecrown,lootapalooza,gilneas,boomsday} ...]], --set [{basic,classic,kara,og,tgt,loe,brm,gvg,naxx,gadget,ungoro,icecrown,lootapalooza,gilneas,boomsday} [{basic,classic,kara,og,tgt,loe,brm,gvg,naxx,gadget,ungoro,icecrown,lootapalooza,gilneas,boomsday} ...]]
                        card set
  -r [{dragon,mech,totem,demon,pirate,murloc,beast,elemental} [{dragon,mech,totem,demon,pirate,murloc,beast,elemental} ...]], --race [{dragon,mech,totem,demon,pirate,murloc,beast,elemental} [{dragon,mech,totem,demon,pirate,murloc,beast,elemental} ...]]
                        filter race
  -rr [{free,common,rare,epic,legendary} [{free,common,rare,epic,legendary} ...]], --rarity [{free,common,rare,epic,legendary} [{free,common,rare,epic,legendary} ...]]
                        filter by card rarity
  -c [{neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid} [{neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid} ...]], --class [{neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid} [{neutral,warrior,priest,hunter,rogue,paladin,shaman,mage,warlock,druid} ...]]
                        filter by class
  -i, --image           [Experimental] show card images using w3mimgdisplay
  -d, --debug           active debug log
```

### Example
* List **Overload Epic** or **Legendary** **Weapon** or **Spell** cards:
```hsSearch.py Overload -rr epic legendary -tp weapon spell```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage1.png "use case 1")

* List **8-10 Attack** point cards in both **wild** and **standard**, card set **GVG** and **KARA**:
```hsSearch.py -a 8 9 10 -f wild standard -s gvg kara```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage2.png "use case 2")

* List **Medivh** card with **Neutral** class and **Mage** class:
```hsSearch.py medivh -c neutral mage```
![Alt text](https://github.com/KrazyCavin/hsSearch/blob/master/example/usage3.png "use case 3")

### [Experimental] Show card images in console
With option **-i**, script will show card images. The idea is using w3mimgdisplay to display image **above** console. The result looks nice but actually it's still not perfect...
