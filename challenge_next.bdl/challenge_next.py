
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

wasSweep = False

def leave (victory, fail):
    # posi_fail = common.matchImg("fight_fail.png")
    # posi_victory = common.matchImg("fight_victory.png")
    posi_leave = common.matchImg("leave.png")

    if victory[0]:
        common.click(posi_leave)
        return True
    if fail[0]:
        common.myPrint("challenge failed")
        common.click(posi_leave)
        return False

def ensure():
    ''' 确认 '''
    common.myPrint("challenge successed")
    common.click(common.matchImg("ensure.png"))

def next():
    common.myPrint("next challenge")
    common.click(common.matchImg("challenge_next.png"))

def sweep():
    global wasSweep
    if wasSweep:
        return True
    else:
        posi = common.matchImg("sweep.png")
        if posi[0]:
            common.click(posi)
            wasSweep = True

def challengeNext():
    common.myPrint("script start")
    common.mySleep(2)
    while(True):
        # 是否在战斗中
        fightRes = common.onFighting()
        if not fightRes[0]:
            if not leave(fightRes[1], fightRes[2]):
                common.myPrint("challenge end")
                break
            sweep()
            ensure()
            next()
        common.mySleep(1)


challengeNext()

common.device.disconnect()






























