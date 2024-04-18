import threading
from PIL import Image
import pyautogui
import time
from .screenshot import screenshot
import io


import numpy as np


def _test_screenshot(result):
    image_bytes, left_top = result
    assert isinstance(image_bytes, bytes)
    image_bytes = np.array(Image.open(io.BytesIO(image_bytes)))
    assert (image_bytes != image_bytes[0, 0]).any()
    image = Image.fromarray(image_bytes)
    assert image.width > 0 and image.height > 0
    image.show()
    screenWidth, screenHeight = pyautogui.size()
    if image.width < screenWidth or image.height < screenHeight:
        assert left_top != (0, 0)
    else:
        assert left_top == (0, 0)


def test_screenshot():
    result = screenshot()
    # check full screen have some content but not empty full one color
    _test_screenshot(result)

    window_name = "测试窗口截图功能的页面"

    def show_window():
        pyautogui.alert(text="", title=window_name, timeout=7000)

    time.sleep(3)
    threading.Thread(target=show_window).start()
    time.sleep(3)
    result = screenshot(window_name=window_name)
    _test_screenshot(result)
