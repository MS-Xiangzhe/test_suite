import threading
from PIL import Image
import pyautogui
import time
from .screenshot import screenshot, screenshot_and_save, _get_screenshot_by_url


def _test_screenshot(image_np):
    assert (image_np != image_np[0, 0]).any()
    image = Image.fromarray(image_np)
    assert image.width > 0 and image.height > 0
    image.show()


def test_screenshot():
    full_image = screenshot()
    print(type(full_image))
    # check full screen have some content but not empty full one color
    _test_screenshot(full_image)

    window_name = "测试窗口截图功能的页面"

    def show_window():
        pyautogui.alert(text="", title=window_name, timeout=5000)

    threading.Thread(target=show_window).start()
    time.sleep(3)
    window_image = screenshot(window_name=window_name)
    _test_screenshot(window_image)
    assert False
