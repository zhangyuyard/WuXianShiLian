#!/usr/bin/python3

import time, os, sys
pwd = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"
try:
    pwd = os.getcwd().strip()
    li = pwd.split("/")
    if len(li) <= 2:
        pwd = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"
except:
    pwd = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"
finally:
    sys.path.append(pwd)

from utility.experience import *

def identifyCoordinate():
    p = matchImg("adventure_boss.png")
    if p[0]:
        return ([p[0] + p[2], p[1] + p[3],])
    return (False,)


coordinate = identifyCoordinate()
if coordinate[0]:
    mainFight(coordinate, 10)
    # mainFight(coordinate, 500)

device.disconnect()































