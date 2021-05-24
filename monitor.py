import time

import pyautogui as pag


def get_panel_size(desc=""):
    # TODO gaicheng anxia he taiqi huode liangge dian

    print("三秒后,将鼠标移动{}".format(desc))
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    # print("请点击.")
    x, y = pag.position()
    print("已获取到坐标({}, {})".format(x, y))

    return "{},{}".format(x, y)


def mouse_click_(position: str = ""):
    x, y = position.split(",")
    x, y = int(x), int(y)
    pag.click(x, y, clicks=3, interval=0.35)


def move_back_(x, y):
    print(x-15, y-15)
    # pag.click(x-15, y-15)
    pag.moveTo(x, y)
    print(x, y)


if __name__ == '__main__':
    # pag.moveTo(0,0)
    # pag.leftClick()
    move_back_(1333, 516)
    while True:
        print(pag.position())
        x, y = pag.position()
        # if x < 720:
        #     pag.click(x, y, clicks=3, interval=0.35)
        time.sleep(3)
