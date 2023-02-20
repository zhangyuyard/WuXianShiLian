#!/usr/bin/python3


from zxtouch.client import zxtouch
from zxtouch.touchtypes import *
from zxtouch.toasttypes import *
import time, os, sys

addrs = [
"127.0.0.1", #手机本地
"10.1.227.102", #客户端IP
"192.168.8.151", #客户端IP
]
ipAddr = addrs[2]
device = zxtouch(ipAddr) # create instance
#device = zxtouch(addrs[1]) # create instance

rootPath = "/private/var/mobile/Library/ZXTouch/scripts/wxxx/"

def restAround():
    posi = matchImg("rest_around.png")
    if posi[0]:
        click(posi)

# 是否勾选自动战斗
wasAuto = False
def checkAutoFight():
    restAround()
    global wasAuto
    if not wasAuto:
        posi = matchImg("autofight_on.png", 0.95)
        if not posi[0]:
            posi = matchImg("autofight_off.png", 0.95)
            if posi[0]:
                click(posi)
                wasAuto = True

def mySleep(secs):
    if ipAddr != "127.0.0.1":
        time.sleep(secs)
    else:
        device.accurate_usleep(secs * 1000)

def myPrint(text, delay = 10):
    if ipAddr != "127.0.0.1":
        print(text)
    else:
        device.show_toast(TOAST_MESSAGE, text, delay)

def click(pos, delay=1):
    if pos[0]:
        device.touch(TOUCH_DOWN, 1, pos[0], pos[1])
        mySleep(0.1)
        device.touch(TOUCH_UP, 1, pos[0], pos[1])
        mySleep(delay)

def matchImg(path, acceptable_value=0.8, max_try_times=5, scaleRation=0.8):
    # 图片长宽不可过大，否则报错，string index out of range
    try:
        template_path = f'{rootPath}images/{path}'
        # myPrint(path)
        result_tuple = device.image_match(template_path, acceptable_value, max_try_times, scaleRation)
    except Exception as err:
        myPrint(type(err))
        errTxt = f'matchImg error: {err}'
        myPrint(errTxt)
        return [False, errTxt]
    if not result_tuple[0]:
        # print("Error happens while matching template image. Error info: " + result_tuple[1])
        return [False, "Error happens while matching template image. Error info: " + result_tuple[1]]
    else:
        result_dict = result_tuple[1]
        if float(result_dict["width"]) != 0 and float(result_dict["height"]) != 0:
            # print("Match success! [" + path.split(".")[0] + "] X: " + result_dict["x"] + ". Y: " + result_dict["y"] + ". Width: " + result_dict["width"] + ". Height: " + result_dict["height"])
            return [float(result_dict["x"]), float(result_dict["y"]), float(result_dict["width"]), float(result_dict["height"])]
        else:
            # print("Match failed. Cannot find template image on screen.")
            return [False, "Match failed. Cannot find template image on screen."]

def onFighting():
    restAround()
    posi = matchImg("autofight_on.png", 0.95)
    if posi[0]:
        return True
    else:
        posi = matchImg("autofight_off.png", 0.95)
        if posi[0]:
            return True
    return False





































