from enum import Enum
import pyautogui


class Button(Enum):
    LEFT = pyautogui.LEFT
    MIDDLE = pyautogui.MIDDLE
    RIGHT = pyautogui.RIGHT
    PRIMARY = pyautogui.PRIMARY
    SECONDARY = pyautogui.SECONDARY


class MouseAction(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    MOVE_TO = "move_to"
    DRAG_TO = "drag_to"
    SCROLL = "scroll"

    @staticmethod
    def str_to_enum(action_str: str) -> "MouseAction":
        return getattr(MouseAction, action_str.upper(), None)


def click(x, y, button=Button.LEFT):
    pyautogui.click(x, y, button=button.value)


def double_click(x, y, button=Button.LEFT, interval=0.0):
    pyautogui.doubleClick(x, y, button=button, interval=interval)


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


def action(
    action: MouseAction,
    x: int = None,
    y: int = None,
    button: Button = Button.LEFT,
    interval: float = 0.0,
    over_time: float = 0.0,
    length: int = None,
    direction: ScrollDirection = None,
):
    if action == MouseAction.CLICK:
        click(x, y, button)
    elif action == MouseAction.DOUBLE_CLICK:
        double_click(x, y, button, interval)
    elif action == MouseAction.MOVE_TO:
        move_to(x, y)
    elif action == MouseAction.DRAG_TO:
        drag_to(x, y, button, over_time)
    elif action == MouseAction.SCROLL:
        scroll(length, direction)
    else:
        raise ValueError(f"Unknown action: {action}")
