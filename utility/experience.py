#!/usr/bin/python3

# 历练
from utility.common import *

def leave (straight = False):
    '''战斗结束 离开'''
    t_s = time.perf_counter()
    while(True):
        t_e = time.perf_counter()
        t_diff = round(t_e - t_s, 2)
        myPrint("on fighting..." + str(t_diff))

        posi_fail = matchImg("fight_fail.png")
        posi_victory = matchImg("fight_victory.png")
        
        if posi_fail[0]:
            break
        if posi_victory[0]:
            break
        if not onFighting():
            break
        if (t_diff > 90):
            break
    posi_leave = matchImg("leave.png")
    # 直接离开，没有战利品
    if straight:
        click(posi_leave)
        return False
    else:
        # 战斗失败，没有战利品
        if posi_fail[0]:
            click(posi_leave)
            return False
        if posi_victory[0]:
            click(posi_leave)
            return True
    return True


timeStar = 0
timeEnd = 0
def fightBegin(coordinate, times, count = 0, fail = 0):
    global timeStar
    global timeEnd
    count += 1
    myPrint("round " + str(count) + " begin")
    timeStar = time.perf_counter()

    click(coordinate)
    checkAutoFight()
    res = fightEnd()
    times -= 1
    timeEnd = time.perf_counter()
    if res:
        myPrint("round " + str(count) + " end(" + str(round(timeEnd - timeStar, 2)) + "s)")
    else:
        fail += 1
        times += 1
        myPrint("round " + str(count) + " end(" + str(round(timeEnd - timeStar, 2)) + "s) failed")

    if not times:
        myPrint("fight end: victory: " + str(count - fail) + "｜defect：" + str(fail))
        return True
    else:
        mySleep(1)
        fightBegin(coordinate, times, count, fail)

def pickupAndClose():
    myPrint("pick up all")
    t_s = time.perf_counter()
    while(True):
        t_e = time.perf_counter()
        t_diff = round(t_e - t_s, 2)
        posi = matchImg("pickupandclose.png")
        if (t_diff > 5):
            break
        if posi[0]:
            click(posi)
            break
    return posi[0]

def fightEnd():
    myPrint("is fight end ?")
    res = leave(False)
    if res:
        res = pickupAndClose()
        if res:
            myPrint("", 1)
        return res
    else:
        myPrint("", 1)
        return res

def mainFight(coordinate, times):
    mySleep(2)
    myPrint("script begin")
    if coordinate:
        fightBegin(coordinate, times)








































