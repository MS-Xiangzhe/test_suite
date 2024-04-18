import numpy
import cv2
from data_processing.src.helpers_inst.raw_control_rpc import mouse_event
from .raw_control_rpc import screenshot
from ..image.cv2utils import get_target_loc
from ..image.ocr.ocrutils import ocr_image_data


def click_on_image(image_path: str, threshold: float = 0.7, click_event="double_click"):
    screen, _ = screenshot()
    image_array = numpy.array(screen)
    target_image = cv2.imread(image_path)
    loc_list = get_target_loc(image_array, target_image, threshold)
    if loc_list:
        for loc in loc_list:
            x_center = loc[0] + target_image.shape[1] // 2
            y_center = loc[1] + target_image.shape[0] // 2

            mouse_event(click_event, x_center, y_center, "left", 0, 0, 0, "")
        return True


def click_on_text(text: str, lang: str = "eng", click_event="double_click"):
    screen, _ = screenshot()
    image_array = numpy.array(screen)
    boxes = ocr_image_data(image_array, lang)

    for box in boxes:
        if box["text"] == text:
            x_center = box["left"] + box["width"] // 2
            y_center = box["top"] + box["height"] // 2

            mouse_event(click_event, x_center, y_center, "left", 0, 0, 0, "")
            return True

    return False
