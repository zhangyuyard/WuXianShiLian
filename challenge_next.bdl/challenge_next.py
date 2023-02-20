
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

from utility.common import *


def leave (straight = False):
    posi_fail = matchImg("fight_fail.png")
    posi_victory = matchImg("fight_victory.png")
    posi_leave = matchImg("leave.png")

    if straight:
        click(posi_leave)
        return True
    else:
        if posi_fail[0]:
            click(posi_leave)
            return False
        if posi_victory[0]:
            myPrint("challenge failed")
            click(posi_leave)
            return True
    return True

def ensure():
    ''' 确认 '''
    myPrint("challenge successed")
    click(matchImg("ensure.png"))
def next():
    myPrint("next challenge")
    click(matchImg("challenge_next.png"))
    checkAutoFight()

def sweep():
    posi = matchImg("sweep.png")
    if posi[0]:
        click(posi)

def challengeNext():
    myPrint("script start")
    mySleep(2)
    sweep()
    mySleep(2)
    next()
    while(True):
        res = leave()
        ensure()
        next()
        if not res:
            myPrint("challenge end")
            break
        mySleep(1)
            

challengeNext()

device.disconnect()






























