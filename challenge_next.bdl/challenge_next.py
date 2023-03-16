
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

    if fail[0]:
        common.myPrint("challenge failed")
        common.click(posi_leave)
        return False # 失败则会结束挑战，否则继续
    else:
        if victory[0]:
            common.click(posi_leave)
        return True

def ensure():
    ''' 确认 '''
    posi = common.matchImg("ensure.png")
    if posi[0]:
        common.click(posi)
        common.myPrint("confirm to getting some things")

def next(times):
    posi = common.matchImg("challenge_next.png")
    if posi[0]:
        common.click(posi)
        times += 1
        common.myPrint(f"challenge successed {times}, go to next challenge")
    return times



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
    times = 0
    while(True):
        # 是否在战斗中
        fightRes = common.onFighting()
        if not fightRes[0]:
            if not leave(fightRes[1], fightRes[2]):
                common.myPrint("challenge end")
                break
            sweep()
            ensure()
            times = next(times)
        common.mySleep(1)
    common.myPrint(f"challenging is done, sum of {times}")


challengeNext()

common.device.disconnect()






























