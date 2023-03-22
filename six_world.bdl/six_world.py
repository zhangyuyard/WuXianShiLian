#!/usr/bin/python3

# code example
# from zxtouch.client import zxtouch
# from zxtouch.touchtypes import *
# from zxtouch.toasttypes import *
# import _thread
import threading

import time, os, sys, random
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
import utility.adventure as adventure
import utility.experience as experience

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
catchingEnd = False

threadLock = threading.Lock()


def checkStuck():
    global isStuck
    # 战斗结束
    res = fightEnd()
    if res:
        isStuck = 0
        setCurStatus("PRE_READY")
        return 
    # 拾取
    posi = common.matchImg("pickupandclose.png")
    if posi[0]:
        common.click(posi)
        setCurStatus("PRE_READY")
        isStuck = 0
        return
    # 选地图
    posi = common.matchImg("sw_select_map_panel.png")
    if posi[0]:
        setCurStatus("END")
        isStuck = 0
        return
    # 什么都没有，可能识图误判，回归流程
    setCurStatus("PRE_READY")
    return

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
    posi = experience.pickupAndClose()
    setCurStatus("PRE_READY")
    return posi

def fightEnd():
    res = experience.fightEnd()
    if res[0] == True:
        return True
    elif res[0] == False:
        setCurStatus("END")
        return False
    elif res[0] == 2:
        # 没成功也没失败，返回到PRE_READY
        setCurStatus("PRE_READY")
        return 2
    

def clickSixWorld(posi):
    common.myPrint("find and click six workd btn")
    # posi = common.matchImg("sw.png")
    if posi[0]:
        common.myPrint("click and enter to sw")
        common.click(posi)
        return True
    return False

def clickAllButton():
    common.click(common.matchImg("sw_all_button.png"))

def checkMapLevel(le = 0):
    global curLevel
    global maxLevel
    le = le | 4 #默认从4级图开始
    curLevel = le
    clickAllButton()
    posi = [False,]
    while(le > 0):
        common.myPrint(f"trying to find a map, current map level is {le}")
        tempPath = f'sw_level_{le}.png'
        posi = common.matchImg(tempPath)
        if posi[0]:
            curLevel = le
            break
        else:
            le += 1
            if le > maxLevel:
                le = -1
        common.mySleep(0.1)
    if le < 0:
        return [False,]
    else:
        return posi

def clickMap():
    pos = common.matchImg("sw_unselect_map.png") # 第一张地图未被选中
    pos2 = common.matchImg("sw_selected_map.png") # 第一张地图被选中
    if pos[0] or pos2[0]:
        common.myPrint("there have a map at least")
        posi = checkMapLevel()
        if posi[0]:
            common.myPrint("finally find to current map level: " + str(curLevel))
            common.click(posi)
            return True
    else:
        return False

def enterMap():
    res = clickMap()
    if not res:
        common.myPrint("maybe maps are gone, prepare exit immediately")
        return False
    posi = common.matchImg("sw_map_entrance.png")
    if posi[0]:
        common.myPrint("find the 'entrance' and click now")
        common.click(posi)
        return True
    return False

def questDone():
    global Position
    global isStuck
    common.myPrint("questDone", 1)
    posi = common.matchImg("sw_quest_done.png")
    # 探索度100%
    if posi[0]:
        # 离开地图按钮
        cache = Position["sw_leave_map"]
        if not cache:
            cache = common.matchImg("sw_leave_map.png")
            if cache[0]:
                Position["sw_leave_map"] = cache
                common.click(cache)
                setCurStatus("END")
            else:
                if isStuck == 1: # 没找到怪，又没找到退出地图
                    isStuck = 2
                setCurStatus("PRE_READY")
            return True
        else:
            common.click(cache)
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
        common.myPrint("maybe is stuck, leaving...")
        setCurStatus("PAUSE")
        checkStuck()
        return
    while(True):
        t_passed = int(float(time.perf_counter() - t_start))
        common.myPrint("seek in monster " + str(t_passed), 2)
        if t_passed > 2 or curStatus == StatusDict["END"]:
            break

        posi = common.matchImg("sw_white_border.png")
        if not posi[0]:
            posi = common.matchImg("sw_blue_border.png")

        if posi[0]:
            break

    if posi[0]:
        isStuck = 0
        mapPosi = [posi[0] + posi[2] * 2, posi[1] + (posi[3] / 2)]
        common.click(mapPosi)
        common.myPrint("click Monster Card")
        setCurStatus("READY")
    else:
        # 未找到怪物
        isStuck = 1 # 作为异常，记录一次
        common.myPrint("not found monster card")
        questDone()

def withFight():
    '''普通战斗'''
    # 普通战斗
    posi = common.matchImg("sw_with_fight.png")
    if posi[0]:
        common.myPrint("batter with sb")
        Position["sw_with_fight"] = posi
        common.click(posi)
        fightEnd()
        return True

    # 遇到宠物
    pet = common.matchImg("sw_catch_pet.png")
    if pet[0]:
        common.click(pet)
        setCurStatus("PETS")
        return True

    setCurStatus("TREASURE")
    return False

def treasure():
    '''打开宝箱'''
    common.myPrint("treasure")
    posi = common.matchImg("sw_try_to_open.png")
    if posi[0]:
        common.click(posi)
        pickupAndClose()
        setCurStatus("PRE_READY")
        return True
    setCurStatus("EVENTS")
    return False

def distinguishBattleKind():
    '''各类奇遇分别处理'''
    global curLevel
    adventure.adventureType(curLevel)

    setCurStatus("ALTAR")

def touchAltar():
    '''神坛'''
    common.myPrint("touchAltar")
    posi = common.matchImg("sw_touch_buff.png")
    if posi[0]:
        common.click(posi)
        setCurStatus("PRE_READY")
        return True
    setCurStatus("PETS")
    return False

def closePets():
    global catchingEnd
    # 抓到或逃跑 抓宠结束
    closeBtn = common.matchImg("sw_pet_escape.png") # 关闭按钮
    if closeBtn[0]:
        common.myPrint(f"press the close button")
        common.click(closeBtn)
        catchingEnd = True
        return True
    # if curStatus != StatusDict["PAUSE"]:
    #     setCurStatus("PRE_READY")
    common.myPrint(f"not find the closeBtn")
    return False

def catchBtn():
    global Position
    if Position["sw_catching_pet"]:
        cbtn = Position["sw_catching_pet"]
    else:
        cbtn = common.matchImg("sw_catching_pet.png")
        if cbtn[0]:
            Position["sw_catching_pet"] = cbtn

    if cbtn[0]:
        common.click(cbtn)
        common.myPrint(f"touch catchBtn")
        return True
    return False

def findPetPoint(idx):
    if catchingEnd:
        return True
    with threadLock:
        p = common.matchImg("sw_catched.png", 0.95, 10)
        common.myPrint(f"thread {idx} working now...")
        if p[0]:
            catchBtn()
            closePets() # 点击 关闭
            common.myPrint(f"thread {idx} find pet point")
def catchPetsDetail():
    global catchingEnd

    t_start = time.time()
    t_max = random.randrange(5, 15)
    while(True):
        t_passed = common.spendTime(t_start)
        if catchingEnd:
            common.myPrint(f'catching used tiem ... {t_passed}/{t_max}')
            break
        if t_passed > t_max:
            catchBtn()
            closePets() # 点击 关闭
        common.run_threads(findPetPoint)
    setCurStatus("PRE_READY")
    catchingEnd = False

# def catchPetsDetail():
#     global catchingEnd
#     t_start = time.time()
#     while(True):
#         t_passed = int(float(time.time() - t_start))
#         common.myPrint(f'catching used tiem ... {t_passed}')

#         p = common.matchImg("sw_catched.png", 0.95, 10)
#         if p[0] or t_passed > 15 or catchingEnd:
#             catchBtn() # 点击 捕捉
#             break
#     closePets() # 点击 关闭
#     setCurStatus("PRE_READY")

def catchPets():
    '''捕捉宠物'''
    global Position

    posi = common.matchImg("sw_catching_pet.png")
    if posi[0]:
        Position["sw_catching_pet"] = posi
        setCurStatus("PAUSE")
        catchPetsDetail()
    else:
        setCurStatus("PRE_READY")
    return False

def outTheMap():
    global fighting
    common.myPrint("out the map ?")
    posi = common.matchImg("sw_select_map_panel.png")
    # posi = common.matchImg("sw_in_sixworld.png")
    if posi[0]:
        fighting = False
        # setCurStatus("PRE_READY")
        return True
    return False

def inTheMap():
    global fighting
    common.myPrint("perhaps in the map now")
    posi = common.matchImg("sw_leave_map.png") # 离开地图按钮
    if posi[0]:
        common.myPrint("yeah in the map now")
        fighting = True
        setCurStatus("PRE_READY")
        return True
    return False

def noMaps():
    return common.matchImg("sw_no_map.png")

def autofight():
    '''自动触发战斗'''
    global fighting
    global curStatus
    fighting = True
    if curStatus == StatusDict["PAUSE"]:
        ''''''
        common.myPrint("Pause...")
        return False
    if curStatus == StatusDict["FIGHT"]:
        ''''''
        common.myPrint("Fight...")
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
    spend_time = 0
    while(times):
        common.myPrint("current status: " + str(curStatus))
        if fighting:
            if autofight():
                times -= 1
                common.myPrint("current run times: " + str(times))
                common.myPrint(f"spend time: {round(float(time.time() - spend_time), 2)}")
        else:
            if noMaps()[0]:
                common.myPrint('no have any maps')
                break
            loc = whereami()
            if loc[0][0]:
                clickSixWorld(loc[0])
            elif loc[1][0]:
                enter = enterMap()
                if enter:
                    spend_time = time.time()
            elif loc[2][0]:
                inMap = inTheMap()
                if inMap:
                    spend_time = time.time()

    return True

def whereami():
    sw = common.matchImg("sw.png") # 主界面，有“六界”图标
    maps = common.matchImg("sw_select_map_panel.png") # 选地图界面
    quest = common.matchImg("sw_leave_map.png") # 已进入地图
    return [sw, maps, quest]

def mainFight(times):
    common.myPrint("script begin")
    common.mySleep(1)
    enterFight(int(times))


mainFight(common.getConfig("fightTimes", "sixWorld"))

common.device.disconnect()






























