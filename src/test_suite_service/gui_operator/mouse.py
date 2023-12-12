from enum import Enum
import pyautogui


class Button(Enum):
    LEFT = pyautogui.LEFT
    MIDDLE = pyautogui.MIDDLE
    RIGHT = pyautogui.RIGHT
    PRIMARY = pyautogui.PRIMARY
    SECONDARY = pyautogui.SECONDARY


def click(x, y, button=Button.LEFT):
    pyautogui.click(x, y, button=button.value)


def double_click(x, y, button=Button.LEFT, interval=0.0):
    pyautogui.doubleClick(x, y, button=button, internal=interval)


def move_to(x, y):
    pyautogui.moveTo(x, y)


def drag_to(x, y, button=Button.LEFT, over_time=0.0):
    pyautogui.dragTo(x, y, button=button.value, dration=over_time)


class ScrollDirection(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


def scroll(legth: int, direction: ScrollDirection):
    match direction:
        case ScrollDirection.UP:
            pyautogui.scroll(legth)
        case ScrollDirection.DOWN:
            pyautogui.scroll(0 - legth)
        case ScrollDirection.LEFT:
            pyautogui.hsroll(0 - legth)
        case ScrollDirection.RIGHT:
            pyautogui.hsroll(legth)
