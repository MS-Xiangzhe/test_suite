import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def get_target_loc(image, target_image, threshold=0.7) -> list[tuple[int, int]]:
    res = cv2.matchTemplate(image, target_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return list(zip(*loc[::-1]))


def draw_frames_and_save(full_image, target_image, coordinates, output_path):
    for pt in coordinates:
        w, h, *_ = target_image.shape
        bottom_right = (pt[0] + h, pt[1] + w)
        cv2.rectangle(full_image, pt, bottom_right, (0, 0, 255), 2)
    cv2.imwrite(output_path, full_image)


def compare_images(imageA, imageB):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    similarity_index = ssim(grayA, grayB)
    difference_percentage = (1 - similarity_index) * 100
    return difference_percentage


def compare_images_color(imageA, imageB):
    B1, G1, R1 = cv2.split(imageA)
    B2, G2, R2 = cv2.split(imageB)
    ssim_b = ssim(B1, B2)
    ssim_g = ssim(G1, G2)
    ssim_r = ssim(R1, R2)
    similarity_index = (ssim_b + ssim_g + ssim_r) / 3.0
    difference_percentage = (1 - similarity_index) * 100
    return difference_percentage


def _process_color_in_image(image, color_rgb, remove=True):
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Convert the RGB color to HSV
    color_hsv = cv2.cvtColor(np.uint8([[color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]

    # Define a range for the color
    lower = np.array([color_hsv[0] - 10, 100, 100], dtype=np.uint8)
    upper = np.array([color_hsv[0] + 10, 255, 255], dtype=np.uint8)

    # Create a mask for the color
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND the mask and the original image
    if remove:
        result = cv2.bitwise_and(image, image, mask=~mask)
    else:
        result = cv2.bitwise_and(image, image, mask=mask)

    return result


def remove_color_in_image(image, color_rgb):
    return _process_color_in_image(image, color_rgb, remove=True)


def keep_color_in_image(image, color_rgb):
    return _process_color_in_image(image, color_rgb, remove=False)
