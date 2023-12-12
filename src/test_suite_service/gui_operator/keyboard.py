import pyautogui
from enum import Enum


def input(text: str, interval: float = 0.0):
    pyautogui.write(text, interval=interval)


class PressStatus(Enum):
    CLICK = "click"
    DOWN = "down"
    UP = "up"
    HOTKEY = "hotkey"


# Support keys: https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
def press(keys: list[str], status: PressStatus = PressStatus.CLICK):
    if isinstance(keys, str):
        key_list = [keys]
    if status == PressStatus.CLICK:
        pyautogui.press(key_list)
    elif status == PressStatus.DOWN:
        for key in key_list:
            pyautogui.keyDown(key)
    elif status == PressStatus.UP:
        for key in key_list:
            pyautogui.keyUp(key)
    elif status == PressStatus.HOTKEY:
        pyautogui.hotkey(*key_list)
