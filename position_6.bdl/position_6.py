#!/usr/bin/python3


# from zxtouch.client import zxtouch
# from zxtouch.touchtypes import *
# from zxtouch.toasttypes import *

import time, os, sys
pwd = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"
try:
    pwd = os.getcwd().strip()
    li = pwd.split("/")
    if len(li) <= 2:
        pwd = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"
    # device = zxtouch("127.0.0.1") # create instance
    # device.show_toast(TOAST_MESSAGE, pwd, 10)
except:
    pwd = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"
finally:
    sys.path.append(pwd)

import utility.experience as experience
import utility.common as common

def identifyCoordinate():
    p = common.matchImg("adventure_site.png", 0.9)
    if p[0]:
        return (
            [p[0], p[1]],
            [p[0] + p[2] / 2, p[1]],
            [p[0] + p[2], p[1]],
            [p[0], p[1] + p[3]],
            [p[0] + p[2] / 2, p[1] + p[3]],
            [p[0] + p[2], p[1] + p[3]],
        )
    return (False,)
    
coordinate = identifyCoordinate()
if coordinate[0]:
    experience.mainFight(coordinate[5], 99999)
    # experience.mainFight(coordinate[5], 70)
    # experience.mainFight(coordinate[5], 30)

common.device.disconnect()































