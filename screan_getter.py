import time
from PIL import Image, ImageGrab

# from monitor import mouse_position


def grab_screen(p1, p2):
    assert isinstance(p1, tuple) and isinstance(p2, tuple)
    img_ready = ImageGrab.grab(p1+p2)
    # img_ready.show()
    img_ready.save("data/test.png")
    time.sleep(0.5)


if __name__ == '__main__':
    ...