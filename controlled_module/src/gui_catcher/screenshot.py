import pyautogui
import pywinctl as pwc
import io
import cv2
import numpy
from typing import Union


def _active_window(window_title: str) -> Union[pwc.Window, None]:
    try:
        while True:
            window = pwc.getWindowsWithTitle(window_title, condition=pwc.Re.MATCH)[0]
            if not window.isActive:
                window.activate(wait=True)
            return window
    except IndexError:
        return None


def _screenshot(window_name: Union[str, None] = None):
    screenshot = None
    left_top = (0, 0)
    if not window_name:
        screenshot = pyautogui.screenshot()
    else:
        title_regex = rf".*{window_name}.*"
        window = _active_window(title_regex)
        if not window:
            window_title_list = pwc.getAllAppsWindowsTitles()
            raise ValueError(
                f"No window found with name {window_name}. All windows: {window_title_list}"
            )
        bbox = window.bbox
        left_top = (bbox[0], bbox[1])
        screenshot = pyautogui.screenshot(
            region=(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1])
        )
    return screenshot, left_top


def screenshot(window_name: Union[str, None] = None) -> tuple[bytes, tuple[int, int]]:
    pil_image, left_top = _screenshot(window_name)
    cv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)

    # Convert the image to bytes
    is_success, buffer = cv2.imencode(".jpg", cv_image)
    if is_success:
        io_buf = io.BytesIO(buffer)
        return io_buf.read(), left_top
    else:
        raise RuntimeError("Could not convert image to bytes")
