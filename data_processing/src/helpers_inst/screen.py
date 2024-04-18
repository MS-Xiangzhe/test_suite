import cv2
import numpy
from .raw_control_rpc import screenshot
from ..image.ocr.ocrutils import ocr_image_data
from ..image.cv2utils import get_target_loc


def is_text_exist(text: str, lang: str = "eng") -> bool:
    screen, _ = screenshot()
    datas = ocr_image_data(screen, lang)
    for data in datas:
        if text in data["text"]:
            return True
    return False


def is_image_exist(image_path: str, threshold: float = 0.7) -> bool:
    screen, _ = screenshot()
    image_array = numpy.array(screen)
    target_image = cv2.imread(image_path)
    if get_target_loc(image_array, target_image, threshold):
        return True
    return False
