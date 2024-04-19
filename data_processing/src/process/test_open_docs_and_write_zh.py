from .. import helpers
from grpc._channel import _InactiveRpcError
from time import sleep


def open_word():
    # 打开 Word
    helpers.run_command("start winword")
    while True:
        try:
            helpers.screenshot("Word")
            break
        except _InactiveRpcError:
            pass


def new_document():
    # 新建文档
    button_new_path = (
        "data_processing/src/process/files/test_open_docs_and_write_zh/button_new.png"
    )
    while True:
        try:
            if helpers.is_image_exist(button_new_path):
                break
        except _InactiveRpcError:
            pass

    bar_path = (
        "data_processing/src/process/files/test_open_docs_and_write_zh/bar_word.png"
    )
    button_blank_document_path = "data_processing/src/process/files/test_open_docs_and_write_zh/button_blank_document.png"
    while True:
        try:
            helpers.keyboard_event(["ctrl", "n"], "hotkey")
            helpers.click_on_image(button_blank_document_path)
            if helpers.is_image_exist(bar_path):
                break
            sleep(1)
        except _InactiveRpcError:
            pass


def input_text():
    # 使用输入法输入文本
    input_method_path = "data_processing/src/process/files/test_open_docs_and_write_zh/input_method_icon.png"
    try:
        if helpers.is_image_exist(input_method_path):
            helpers.keyboard_event(["win", "space"], "hotkey")
    except _InactiveRpcError:
        pass
    helpers.keyboard_event("Abby ", "click")
    try:
        if not helpers.is_image_exist(input_method_path):
            helpers.keyboard_event(["win", "space"], "hotkey")
    except _InactiveRpcError:
        pass
    helpers.keyboard_event("nihaoya", "click")
    nihao_text = "你好呀"
    while True:
        try:
            helpers.click_on_text(nihao_text, "chi_sim", "click")
            break
        except _InactiveRpcError:
            pass
    helpers.keyboard_event(",", "click")
    helpers.keyboard_event("huanyinghuilai", "click")
    helpers.keyboard_event(["space"], "click")
    helpers.keyboard_event(["enter"], "click")
    try:
        if helpers.is_image_exist(input_method_path):
            helpers.keyboard_event(["win", "space"], "hotkey")
    except _InactiveRpcError:
        pass
    assert helpers.is_text_exist("Abby")


def automate_word():
    open_word()
    new_document()
    input_text()


def test_open_docs_and_write_zh():
    automate_word()
