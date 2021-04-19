import time

import pyautogui as pag


def get_panel_size(position="left_top"):
    # TODO gaicheng anxia he taiqi huode liangge dian

    print("三秒后,将鼠标移动到题目{}角".format("左上" if position == "left_top" else "右下"))
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


if __name__ == '__main__':
    pag.moveTo(0,0)
    pag.leftClick()
    ...
