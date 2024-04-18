from .ocrutils import ocr_image_data
from ..utils import image_from_bytes


def test_ocr_eng():
    path = "tests_data/ocr_eng.png"
    with open(path, "rb") as f:
        image_bytes = f.read()
    image = image_from_bytes(image_bytes)
    boxes = ocr_image_data(image)
    print(boxes)
    assert ".gitignore" in [box["text"] for box in boxes]
    assert "4/18/2024" in [box["text"] for box in boxes]
    assert "1KB" in [box["text"] for box in boxes]
