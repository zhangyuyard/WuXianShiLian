#!/usr/bin/python3


# 六界奇遇事件等

from utility.common import *
from utility.experience import *

def __feilinguan():
    '''飞灵观 直接离开'''
    myPrint("feilinguan")
    posi = matchImg("sw_FeiLinGuan.png")
    if posi[0]:
        leave(True)

def __valley():
    '''valley'''
    myPrint("valley")
    posi = matchImg("sw_under_valley.png")
    if posi[0]:
        posi = matchImg("sw_dash.png")
        if posi[0]:
            click(posi)
            mySleep(0.5)
            return True
        return False
    return False

def __innerHouse():
    '''茅屋内'''
    myPrint("innerHouse")
    posi = matchImg("sw_house_inner.png")
    if posi[0]:
        posi = matchImg("sw_pick_book.png")
        if posi[0]:
            click(posi)
            mySleep(0.5)
            return True
        return False
    return False

def __cliff():
    '''掉入悬崖'''
    myPrint("cliff")
    posi = matchImg("sw_cliff.png")
    if posi[0]:
        posi = matchImg("sw_rush_snake.png")
        if posi[0]:
            click(posi)
            mySleep(0.5)
            __valley()
            __innerHouse()
            return True
        return False
    return False

def __secretCave():
    '''隐秘山洞'''
    myPrint("secretCave")
    posi = matchImg("sw_secret_cave.png")
    if posi[0]:
        if posi[0]:
            # 本职业的奇遇条件不满足，直接离开
            leave(True)
            mySleep(0.5)
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
    myPrint("duxinmang")
    posi = matchImg("sw_DuXinMang.png")
    if posi[0]:
        posi = matchImg("sw_DuXinMang_fight.png")
        if posi[0]:
            click(posi)
            mySleep(0.5)
            fightEnd()
            return True
        return False
    return False

def __xuemomenren():
    '''血魔门人'''
    myPrint("xuemomenren")
    posi = matchImg("sw_XueMoMenRen.png")
    if posi[0]:
        posi = matchImg("sw_xmmr_fight.png")
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
    myPrint("first herb")
    posi = matchImg("sw_herb_fight.png")
    if posi[0]:
        click(posi)
        return False
    return False

def adventureType(level):
    if level == 4:
        __adventure_level_4()
    if level == 7:
        __adventure_level_7()
    else:
        return True