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

# 六界奇遇事件等

import utility.common as common
import utility.experience as experience


def __feilinguan():
    '''飞灵观 直接离开'''
    common.myPrint("feilinguan")
    posi = common.matchImg("sw_FeiLinGuan.png")
    if posi[0]:
        experience.leave(True)

def __valley():
    '''valley'''
    common.myPrint("valley")
    posi = common.matchImg("sw_under_valley.png")
    if posi[0]:
        posi = common.matchImg("sw_dash.png")
        if posi[0]:
            common.click(posi)
            return True
        return False
    return False

def __innerHouse():
    '''茅屋内'''
    common.myPrint("innerHouse")
    posi = common.matchImg("sw_house_inner.png")
    if posi[0]:
        posi = common.matchImg("sw_pick_book.png")
        if posi[0]:
            common.click(posi)
            return True
        return False
    return False

def __cliff():
    '''掉入悬崖'''
    common.myPrint("cliff")
    posi = common.matchImg("sw_cliff.png")
    if posi[0]:
        posi = common.matchImg("sw_rush_snake.png")
        if posi[0]:
            common.click(posi)
            __valley()
            __innerHouse()
            return True
        return False
    return False

def __secretCave():
    '''隐秘山洞'''
    common.myPrint("secretCave")
    posi = common.matchImg("sw_secret_cave.png")
    if posi[0]:
        if posi[0]:
            # 本职业的奇遇条件不满足，直接离开
            experience.leave(True)
            common.mySleep(0.5)
            return True
        # posi = matchImg("sw_push_jade_pendant.png")
        # if posi[0]:
        #     click(posi)
        #     mySleep(0.5)
        #     return True
        # return False
    return False

def __duxinmang():
    '''毒心蟒 战斗'''
    common.myPrint("duxinmang")
    posi = common.matchImg("sw_DuXinMang.png")
    if posi[0]:
        posi = common.matchImg("sw_DuXinMang_fight.png")
        if posi[0]:
            common.click(posi)
            experience.fightEnd()
            return True
        return False
    return False

def __xuemomenren():
    '''血魔门人'''
    common.myPrint("xuemomenren")
    posi = common.matchImg("sw_XueMoMenRen.png")
    if posi[0]:
        posi = common.matchImg("sw_xmmr_fight.png")
        if posi[0]:
            click(posi)
        return False
    return False

def __adventure_level_4():
    # 飞灵观
    __feilinguan()
    # 毒心蟒
    __duxinmang()
    # 掉入悬崖
    __cliff()
    # 血魔门人
    __xuemomenren()
    # 隐秘洞穴
    __secretCave()

def __adventure_level_7():
    common.myPrint("first class herb") # 一品药草
    posi = common.matchImg("sw_herb.png")
    if posi[0]:
        posi = common.matchImg("sw_herb_fight.png")
        if posi[0]:
            common.click(posi)
        return False
    return False

def adventureType(level):
    if level == 4:
        __adventure_level_4()
    if level == 7:
        __adventure_level_7()
    else:
        return True