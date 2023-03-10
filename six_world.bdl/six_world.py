#!/usr/bin/python3

# code example
# from zxtouch.client import zxtouch
# from zxtouch.touchtypes import *
# from zxtouch.toasttypes import *
# import _thread
import threading, multiprocessing

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
from utility.adventure import *
from utility.experience import pickupAndClose

# 缓存的坐标
Position = {
    "sw_leave_map": False,
    "sw_confirm": False,
    "sw_catching_pet": False,
}

# 状态字典
StatusDict = {
    "OUT": -1,
    "PRE_READY": 0, #预备
    "READY": 1, # 准备，寻敌，事件判断
    "FIGHT": 2, # 战斗
    "ROUTINE": 3, # 普通敌人
    "EVENTS": 4, # 奇遇事件
    "PETS": 5, # 捕捉宠物
    "TREASURE": 6, # 宝箱
    "ALTAR": 7, # 神坛，Buff
    "PAUSE": 8, # 暂停
    "END": 9, # 结束

    # FLG, # 飞灵观
    # CLIFF, # 掉入悬崖
    # XMMR, # 血魔门人
}
# 当前地图等级
curLevel = 0
# 最高地图等级
maxLevel = 7
# 当前状态
curStatus = StatusDict["PRE_READY"]
# 卡住了
isStuck = 0

#
fighting = False
# 捕捉宠物是否结束
catchingEnd = True

def checkStuck():
    global isStuck
    # 战斗结束
    posi_fail = matchImg("fight_fail.png")
    posi_victory = matchImg("fight_victory.png")
    if posi_fail[0] or posi_victory[0]:
        posi = matchImg("leave.png")
        if posi[0]:
            click(posi)
            setCurStatus("PRE_READY")
            isStuck = 0
            return
    mySleep(1)
    # 拾取
    mySleep(1)
    posi = matchImg("pickupandclose.png")
    if posi[0]:
        click(posi)
        setCurStatus("PRE_READY")
        isStuck = 0
        return
    mySleep(1)
    # 选地图
    posi = matchImg("sw_select_map_panel.png")
    if posi[0]:
        setCurStatus("END")
        isStuck = 0
        return
    mySleep(1)
    # 什么都没有，可能识图误判，回归流程
    setCurStatus("PRE_READY")
    return

def leave (straight = False):
    '''检测是否战斗结束 离开'''
    if not onFighting():
        # 不在战斗中
        return False
    if outTheMap():
        # 在选地图界面
        setCurStatus("END")
        return False
    t_s = time.perf_counter()
    while(True):
        t_e = time.perf_counter()
        t_diff = round(t_e - t_s, 2)
        myPrint("on fighting..." + str(t_diff))

        if (t_diff > 90):
            break
        posi_fail = matchImg("fight_fail.png")
        posi_victory = matchImg("fight_victory.png")
        posi_leave = matchImg("leave.png")
        # insw = matchImg("sw_in_sixworld.png")
        # if insw[0]:
        #     # 正在选择地图界面
        #     enterMap()
        #     return False
        if posi_fail[0]:
            break
        if posi_victory[0]:
            break
        if posi_leave[0]:
            break

    click(posi_leave)
    # 直接离开，没有战利品
    if straight:
        return False
    else:
        # 战斗失败，没有战利品
        if posi_fail[0]:
            return False
        if posi_victory[0]:
            return True
    return True

def setCurStatus(status):
    global curStatus
    global StatusDict
    if status != "END":
        curStatus = StatusDict[status]
    else:
        curStatus = StatusDict["END"]

def confirm():
    ''' 确定 '''

def pickupAndClose():
    myPrint("pick up all")
    t_s = time.perf_counter()
    while(True):
        t_e = time.perf_counter()
        posi = matchImg("pickupandclose.png")
        if posi[0]:
            click(posi)
            break
        if t_e - t_s > 5:
            break
    setCurStatus("PRE_READY")
    return posi[0]

def fightEnd():
    myPrint("is fight end ?")
    insw = matchImg("sw_in_sixworld.png")
    if insw[0]:
        res = leave(insw[0])
    else:
        res = leave(False)

    if res:
        res = pickupAndClose()
        if res:
            myPrint("", 1)
        return res
    else:
        myPrint("", 1)
        return res
    setCurStatus("PRE_READY")

def clickSixWorld():
    myPrint("is main panel ?")
    posi = matchImg("sw.png")
    if posi[0]:
        myPrint("click and enter to sw")
        click(posi)
        return True
    return False

def clickAllButton():
    click(matchImg("sw_all_button.png"))

def checkMapLevel(le = 0):
    global curLevel
    global maxLevel
    le = le | 4 #默认从4级图开始
    curLevel = le
    clickAllButton()
    posi = [False,]
    while(le > 0):
        tempPath = f'sw_level_{le}.png'
        posi = matchImg(tempPath)
        if posi[0]:
            curLevel = le
            break
        else:
            le = le + 1
            if le > maxLevel:
                le = -1
        mySleep(0.1)
    if le < 0:
        return [False,]
    else:
        return posi

def clickMap():
    pos = matchImg("sw_unselect_map.png")
    if pos[0]:
        myPrint("no have select a map")
        posi = checkMapLevel()
        if posi[0]:
            myPrint("current map level: " + str(curLevel))
            click(posi)
            return True
        # posi = matchImg("sw_first_map.png", 0.9)
        # if posi[0]:
        #     myPrint("choose one map")
        #     mapPosi = [posi[0] + posi[2] / 2, posi[1] + posi[3]]
        #     click(mapPosi)
        #     mySleep(0.5)
        #     return True
        else:
            myPrint("no have any maps")
            # 没有地图了 结束脚本
            return False
    if noMaps():
        myPrint('no have any maps')
        return False
    # 已选择了地图
    myPrint("has select a map")
    return True

def enterMap():
    clickSixWorld()
    checkMapLevel()
    res = clickMap()
    if not res:
        myPrint("maps is none, exit immediately")
        device.disconnect()
        return False
    posi = matchImg("sw_map_entrance.png")
    if posi[0]:
        click(posi)
        return True
    return False

def outTheMap():
    global fighting
    myPrint("out the map ?")
    posi = matchImg("sw_select_map_panel.png")
    # posi = matchImg("sw_in_sixworld.png")
    if posi[0]:
        fighting = False
        # setCurStatus("PRE_READY")
        return True
    return False

def inTheMap():
    global fighting
    myPrint("in the map ?")
    posi = matchImg("sw_leave_map.png")
    if posi[0]:
        fighting = True
        setCurStatus("PRE_READY")
        return True
    return False

def questDone():
    global Position
    global isStuck
    myPrint("questDone", 1)
    posi = matchImg("sw_quest_done.png")
    # 探索度100%
    if posi[0]:
        # 离开地图按钮
        cache = Position["sw_leave_map"]
        if not cache:
            cache = matchImg("sw_leave_map.png")
            if cache[0]:
                Position["sw_leave_map"] = cache
                click(cache)
                setCurStatus("END")
            else:
                if isStuck == 1: # 没找到怪，又没找到退出地图
                    isStuck = 2
                setCurStatus("PRE_READY")
            return True
        else:
            click(cache)
            setCurStatus("END")
    else:
        if isStuck == 1: # 没找到怪，又没找到探索度100%
            isStuck = 2
        setCurStatus("PRE_READY")
    return False

def clickMonsterCard():
    global isStuck
    t_start = time.perf_counter()
    posi = [False, ""]
    # 没找到怪，也没退出，据观察，可能在战斗结束界面，也可能在选择地图界面，leave一下试试
    if isStuck == 2:
        myPrint("maybe is stuck, leaving...")
        checkStuck()
        return
    while(True):
        t_passed = int(float(time.perf_counter() - t_start))
        myPrint("seek in monster " + str(t_passed), 2)
        if t_passed > 2 or curStatus == StatusDict["END"]:
            break

        posi = matchImg("sw_white_border.png")
        if not posi[0]:
            posi = matchImg("sw_blue_border.png")

        if posi[0]:
            break

    if posi[0]:
        isStuck = 0
        mapPosi = [posi[0] + posi[2] * 2, posi[1] + (posi[3] / 2)]
        click(mapPosi)
        myPrint("click Monster Card")
        setCurStatus("READY")
    else:
        # 未找到怪物
        isStuck = 1 # 作为异常，记录一次
        myPrint("not found monster card")
        questDone()

def withFight():
    '''普通战斗'''
    global catchingEnd
    # 普通战斗
    posi = matchImg("sw_with_fight.png")
    if posi[0]:
        myPrint("batter with sb")
        Position["sw_with_fight"] = posi
        click(posi)
        checkAutoFight()
        fightEnd()
        return True

    # 遇到宠物
    pet = matchImg("sw_catch_pet.png")
    if pet[0]:
        catchingEnd = False
        click(pet)
        setCurStatus("PETS")
        return True

    setCurStatus("TREASURE")
    return False

def treasure():
    '''打开宝箱'''
    myPrint("treasure")
    posi = matchImg("sw_try_to_open.png")
    if posi[0]:
        click(posi)
        pickupAndClose()
        return True
    setCurStatus("EVENTS")
    return False

def distinguishBattleKind():
    '''各类奇遇分别处理'''
    global curLevel
    adventureType(curLevel)

    setCurStatus("ALTAR")

def touchAltar():
    '''神坛'''
    myPrint("touchAltar")
    posi = matchImg("sw_touch_buff.png")
    if posi[0]:
        click(posi)
        setCurStatus("PRE_READY")
        return True
    setCurStatus("PETS")
    return False

def closePets():
    # 抓到或逃跑 抓宠结束
    myPrint("look for closeBtn")
    closeBtn = matchImg("sw_pet_escape.png") # 关闭按钮
    if closeBtn[0]:
        myPrint("press the close button")
        click(closeBtn)
        setCurStatus("PRE_READY")
        return True
    if curStatus != StatusDict["PAUSE"]:
        setCurStatus("PRE_READY")
    return False

def catchBtn():
    global Position
    if Position["sw_catching_pet"]:
        cbtn = Position["sw_catching_pet"]
    else:
        cbtn = matchImg("sw_catching_pet.png")
        if cbtn[0]:
            Position["sw_catching_pet"] = cbtn

    if cbtn[0]:
        click(cbtn)
        return True
    return False

def catchPetsDetail():
    global catchingEnd
    t_start = time.time()
    while(True):
        if catchingEnd:
            break
        t_passed = int(float(time.time() - t_start))
        myPrint(f'catching used tiem ... {t_passed}')
        p = matchImg("sw_catched.png", 0.98)
        # if p[0]:
        if p[0] or t_passed > 15:
            myPrint("matching catched condition")
            catchBtn() # 点击 捕捉
            catchingEnd = True
        mySleep(0.001)
    closePets()

def catchPets():
    '''捕捉宠物'''
    global catchingEnd
    global Position

    posi = matchImg("sw_catching_pet.png")
    if posi[0]:
        Position["sw_catching_pet"] = posi
        setCurStatus("PAUSE")
        catchPetsDetail()
    else:
        closePets()
    return False

def noMaps():
    posi = matchImg("sw_no_map.png")
    if posi[0]:
        return True
    else:
        return False

def autofight():
    '''自动触发战斗'''
    global fighting
    fighting = True
    if curStatus == StatusDict["PAUSE"]:
        ''''''
        myPrint("Pause...")
        return False
    if curStatus == StatusDict["PRE_READY"]:
        clickMonsterCard()
        return False
    if curStatus == StatusDict["READY"]:
        withFight()
        return False
    if curStatus == StatusDict["TREASURE"]:
        treasure()
        return False
    if curStatus == StatusDict["EVENTS"]:
        distinguishBattleKind()
        return False
    if curStatus == StatusDict["ALTAR"]:
        touchAltar()
        return False
    if curStatus == StatusDict["PETS"]:
        catchPets()
        return False
    if curStatus == StatusDict["END"]:
        fighting = False
        return True

def enterFight (times):
    global fighting
    while(times):
        if fighting:
            if autofight():
                times -= 1
                myPrint("current run times: " + str(times))
        else:
            enterMap()
            inTheMap()
            noMaps()
        myPrint("current status: " + str(curStatus))

    return True

def mainFight(times = 60):
    myPrint("script begin")
    mySleep(2)
    enterFight(times)


mainFight()

device.disconnect()






























