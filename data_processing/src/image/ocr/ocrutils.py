import pytesseract
from PIL import Image


def ocr_image_data(image: Image, lang: str = "eng"):
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    boxes = []
    n_boxes = len(data["text"])
    for i in range(n_boxes):
        if int(data["conf"][i]) > 60:
            box = {
                "text": data["text"][i],
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
            }
            boxes.append(box)
    return boxes
