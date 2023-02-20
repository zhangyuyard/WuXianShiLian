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

from utility.common import *
# from utility.adventure import *

def test():
    # posi = matchImg("sw_DuXinMang_fight.png")
    # posi = matchImg("autofight_off.png", 0.95)
    # posi = matchImg("autofight_on.png", 0.95)
    # posi = matchImg("sw_blue_border.png")
    # posi = matchImg("sw_white_border.png")
    posi = matchImg("sw_no_map.png")
    return posi


test()