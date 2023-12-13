import pyautogui
import win32gui
import cv2
import numpy


def _screenshot(window_name: str or None = None):
    if window_name is None:
        return pyautogui.screenshot()

    toplist, winlist = [], []

    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)

    window_list = [(hwnd, title) for hwnd, title in winlist if window_name in title]
    # just grab the hwnd for first window matching firefox
    window_list = window_list[0]
    hwnd = window_list[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    return pyautogui.screenshot(
        region=(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1])
    )


def screenshot(window_name: str or None = None):
    pil_image = _screenshot(window_name)
    return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)


# TODO: thread safe
GLOBAL_SCREENSHOT_MAP = {}
SCREENSHOT_URL_PREFIX = "mem://screenshot/"


def screenshot_and_save(window_name: str, filename: str) -> str:
    img = screenshot(window_name)
    if filename:
        img.save(filename)
        return filename
    i = max(GLOBAL_SCREENSHOT_MAP.keys() + [-1]) + 1
    GLOBAL_SCREENSHOT_MAP[i] = img
    return SCREENSHOT_URL_PREFIX + str(i)


def _get_screenshot_by_url(url: str):
    if url.startswith(SCREENSHOT_URL_PREFIX):
        return GLOBAL_SCREENSHOT_MAP[int(url[len(SCREENSHOT_URL_PREFIX) :])]
    return None
