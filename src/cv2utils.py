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
