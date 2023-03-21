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

import utility.experience as experience
import utility.common as common

def identifyCoordinate():
    p = common.matchImg("adventure_boss.png")
    if p[0]:
        return ([p[0] + p[2], p[1] + p[3],])
    return (False,)


coordinate = identifyCoordinate()
if coordinate[0]:
    experience.mainFight(coordinate, common.getConfig("fightTimes", "boss"))
    # experience.mainFight(coordinate, 500)

common.device.disconnect()































