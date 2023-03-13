
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

import utility.common as common


def leave (straight = False):
    posi_fail = common.matchImg("fight_fail.png")
    posi_victory = common.matchImg("fight_victory.png")
    posi_leave = common.matchImg("leave.png")

    if straight:
        common.click(posi_leave)
        return True
    else:
        if posi_fail[0]:
            common.myPrint("challenge failed")
            common.click(posi_leave)
            return False
        if posi_victory[0]:
            common.click(posi_leave)
            return True
    return True

def ensure():
    ''' 确认 '''
    common.myPrint("challenge successed")
    common.click(matchImg("ensure.png"))

def next():
    common.myPrint("next challenge")
    common.click(matchImg("challenge_next.png"))
    common.checkAutoFight()

def sweep():
    posi = common.matchImg("sweep.png")
    if posi[0]:
        common.click(posi)

def challengeNext():
    common.myPrint("script start")
    common.mySleep(2)
    sweep()
    ensure()
    next()
    while(True):
        res = leave()
        ensure()
        next()
        if not res:
            common.myPrint("challenge end")
            break
        common.mySleep(1)


challengeNext()

device.disconnect()






























