from typing import Union
from PIL.Image import Image
from controlled_module.src.gui_operator.keyboard import PressStatus
from controlled_module.src.gui_operator.mouse import MouseAction
from data_processing.src.helpers_inst import clicker
from .helpers_inst import raw_control_rpc as rpc
from .helpers_inst import screen


def screenshot(window_name: Union[str, None] = None) -> tuple[Image, tuple[int, int]]:
    return rpc.screenshot(window_name)


def keyboard_event(keys: list[str], action: PressStatus = PressStatus.CLICK):
    rpc.keyboard_event(keys, action)


def mouse_event(
    action: MouseAction,
    x: int,
    y: int,
    button: str,
    interval: int,
    over_time: int,
    length: int,
    direction: str,
):
    rpc.mouse_event(action, x, y, button, interval, over_time, length, direction)


def run_command(command: str) -> tuple[int, str, str]:
    return rpc.run_command(command)


def is_text_exist(text: str, lang: str = "eng") -> bool:
    return screen.is_text_exist(text, lang)


def is_image_exist(image_path: str, threshold: float = 0.7) -> bool:
    return screen.is_image_exist(image_path, threshold)


def click_on_image(image_path: str, threshold: float = 0.7, click_event="double_click"):
    return clicker.click_on_image(image_path, threshold, click_event)


def click_on_text(text: str, lang: str = "eng", click_event="double_click"):
    return clicker.click_on_text(text, lang, click_event)
