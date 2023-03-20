#!/usr/bin/python3


from zxtouch.client import zxtouch
from zxtouch.touchtypes import *
from zxtouch.toasttypes import *
import time, os, sys
import threading
import multiprocessing
import re
import configparser

# 获取当前工作目录
cwd = os.getcwd()
# 拼接配置文件路径
config_path = os.path.join(cwd, 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)
# 获取配置项
ipAddr = config.get('addrs', 'client')
rootPath = config.get('path', 'rootPath')


# addrs = [
# "127.0.0.1", #手机本地
# "10.1.227.102", #客户端IP
# "192.168.8.199", #客户端IP
# ]

device = zxtouch(ipAddr) # create instance

# 是否勾选自动战斗
wasAuto = False
def restAround():
    posi = matchImg("rest_around.png")
    if posi[0]:
        click(posi)

def checkAutoFight():
    global wasAuto
    restAround()
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
# utils
def safe_float(s):
    try:
        return float(s)
    except ValueError:
        nums, other = nusplit_and_convert(s)
        return nums  # 转换失败，返回默认值
def split_and_convert(s):
    pattern = r'([\d\.]+)'  # 匹配数字和小数点的正则表达式
    nums = re.findall(pattern, s, re.DOTALL)  # 查找所有匹配的数字和小数点
    nums = [float(num) for num in nums]  # 将数字列表中的字符串转换为浮点数
    other = re.sub(pattern, '', s, flags=re.DOTALL)  # 将字符串中的数字和小数点替换为空，得到剩余的字符
    return nums, other

def matchImg(path, acceptable_value=0.8, max_try_times=5, scaleRation=0.8):
    # 图片长宽不可过大，否则报错，string index out of range
    try:
        template_path = f'{rootPath}images/{path}'
        # myPrint(path)
        result_tuple = device.image_match(template_path, acceptable_value, max_try_times, scaleRation)
        if not result_tuple[0]:
        # print("Error happens while matching template image. Error info: " + result_tuple[1])
            return [False, "Error happens while matching template image. Error info: " + result_tuple[1]]
        else:
            result_dict = result_tuple[1]
            x = safe_float(result_dict["x"])
            y = safe_float(result_dict["y"])
            width = safe_float(result_dict["width"])
            height = safe_float(result_dict["height"])
            if width != 0 and height != 0:
                # print("Match success! [" + path.split(".")[0] + "] X: " + result_dict["x"] + ". Y: " + result_dict["y"] + ". Width: " + result_dict["width"] + ". Height: " + result_dict["height"])
                return [x, y, width, height]
            else:
                # print("Match failed. Cannot find template image on screen.")
                return [False, "Match failed. Cannot find template image on screen."]
    except Exception as err:
        myPrint(type(err))
        errTxt = f'matchImg({path}) error: {err}'
        myPrint(errTxt)
        return [False, errTxt]

def onFighting():
    checkAutoFight()
    fightOn = matchImg("autofight_on.png", 0.95)
    fightOff = matchImg("autofight_off.png", 0.95)
    posi_fail = matchImg("fight_fail.png")
    posi_victory = matchImg("fight_victory.png")
    if not posi_fail[0] and not posi_victory[0]:
        if fightOn[0] or fightOff[0]:
            # 战斗未结束 并且 有“自动战斗”标识 则说明正在战斗中
            return [True, posi_victory, posi_fail]
        else:
            return [False, posi_victory, posi_fail]
    else:
        return [False, posi_victory, posi_fail]

def run_threads(funcName):
    def wrapFunc(idx):
        try:
            funcName(idx)
        finally:
            return True

    num_threads = multiprocessing.cpu_count()
    # num_threads = multiprocessing.cpu_count() / 2
    threads = []
    for i in range(max(round(num_threads), 2)):
        my_args = (i,)
        thread = threading.Thread(target=wrapFunc, args=my_args)
        thread.start()
        threads.append(thread)
    for thread in threads:
        # myPrint(f"launch thread-{thread}")
        thread.join()

def spendTime(t_start):
    return round(time.time() - t_start, 2)





































