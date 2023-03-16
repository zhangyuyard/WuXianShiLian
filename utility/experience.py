#!/usr/bin/python3

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
# 历练
import utility.common as common

# 缓存的坐标
Position = {
    "leave": [False,],
}

def leavePosi():
    global Position
    posi_leave = []
    if Position["leave"][0]:
        posi_leave = Position["leave"]
    else:
        posi_leave = common.matchImg("leave.png")
        Position["leave"] = posi_leave
    return posi_leave

def leave (straight = False):
    '''战斗结束 离开'''
    global Position
    fightRes = []
    posi_leave = leavePosi()
    # 直接离开，没有战利品
    if straight:
        common.myPrint("direactly quit without fight")
        common.click(posi_leave)
        return -1
    else:
        t_s = time.time()
        while(True):
            t_diff = common.spendTime(t_s)
            fightRes = common.onFighting()
            if not fightRes[0]:
                break
            common.myPrint(f"on fighting...{t_diff}")
            if (t_diff > 90): # 一场战斗最多90s
                break

        posi_leave = leavePosi()
        # posi_victory = common.matchImg("fight_victory.png")
        if fightRes[1][0]:
            common.myPrint("fighting victory")
            common.click(posi_leave)
            return 1 # 需要拾取战利品，返回True
        # posi_fail = common.matchImg("fight_fail.png")
        # 战斗失败，没有战利品
        if fightRes[2][0]:
            common.myPrint("fighting failure")
            common.click(posi_leave)
            return 0
    common.myPrint("fighting unkonw")
    return 2 # 既没成功，也没失败，属于异常


timeStar = 0
timeEnd = 0
def fightBegin(coordinate, times, count = 0, fail = 0):
    global timeStar
    global timeEnd
    count += 1
    common.myPrint("round " + str(count) + " begin")
    timeStar = time.time()

    common.click(coordinate)
    isEnd = fightEnd()
    times -= 1
    timeEnd = time.time()
    if isEnd:
        common.myPrint("round " + str(count) + " end(" + str(round(timeEnd - timeStar, 2)) + "s)")
    else:
        fail += 1
        times += 1
        common.myPrint("round " + str(count) + " end(" + str(round(timeEnd - timeStar, 2)) + "s) failed")

    if not times:
        common.myPrint("fight end: victory: " + str(count - fail) + "｜defect：" + str(fail))
        return True
    else:
        fightBegin(coordinate, times, count, fail)

def pickupAndClose():
    common.myPrint("prepare pick up all")
    t_s = time.time()
    while(True):
        t_diff = round(time.time() - t_s, 2)
        posi = common.matchImg("pickupandclose.png")
        if (t_diff > 5):
            break
        if posi[0]:
            common.myPrint("pick up all")
            common.click(posi)
            break
    return True

def fightEnd():
    common.myPrint("is fight end ?")
    awards = leave(False)
    if awards == -1:
        # 没有战利品，直接下一局
        return [True,]
    elif awards == 0:
        # 失败
        return [False,]
    elif awards == 1:
        # 成功 可能有战利品
        return [pickupAndClose(),]
    elif awards == 2:
        # 异常
        return [False,]


def mainFight(coordinate, times):
    common.mySleep(2)
    common.myPrint("script begin")
    if coordinate:
        fightBegin(coordinate, times)








































