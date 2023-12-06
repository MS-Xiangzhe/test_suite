from pathlib import Path
import time
import cv2
from utils import parse_file_name
from cv2utils import get_target_loc, draw_frames_and_save


class TargetImage:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.threshold = 0.7
        self.stop_at_begin = False
        self.is_full = False
        args = parse_file_name(path)
        self.index_list = []
        arg_index = 0
        for arg in args:
            if isinstance(arg, int):
                self.index_list.append(arg)
                arg_index += 1
        if args[-1] == "full":
            self.is_full = True
        if args[arg_index] == "from":
            self.stop_at_begin = True
        try:
            self.threshold = float(args[-1])
        except Exception:
            pass
        self.__image = None
        self.split_coordinate = None

    def __str__(self) -> str:
        return str(self.path)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def image(self):
        if self.__image is None:
            self.__image = cv2.imread(str(self.path))
        return self.__image

    def init_split_coordinate(self, full_image_path: str):
        self.split_coordinate = self.__find_target_in_image(
            full_image_path, str(self.path)
        )
        if self.split_coordinate is None:
            raise Exception(f"Can't find {self.path} in {full_image_path}")

    def test_split_coordinate(
        self, full_image_path: str, result_img_dir_path: str or None = None
    ):
        full_image = cv2.imread(full_image_path)
        coordinate_list = self.get_coordinate_list_in_full_image(full_image)
        if not coordinate_list:
            raise Exception(f"Can't find {self.path} in {full_image_path}")
        if result_img_dir_path:
            full_image = cv2.imread(full_image_path)
            rsl_path = str(
                result_img_dir_path
                / self.path.with_stem(f"{time.time()}_{self.path.stem}").name
            )
            draw_frames_and_save(full_image, self.image, coordinate_list, rsl_path)

    def get_coordinate_list_in_full_image(
        self, full_image: str
    ) -> tuple[(tuple[int, int], tuple[int, int])]:
        tolerance = 0.1
        adjusted_limit = 100
        best_match_percent, bottom_right_percent = self.split_coordinate

        # Get the dimensions of the full image
        full_image_height, full_image_width = full_image.shape[:2]

        adjusted_high = min(full_image_height * tolerance, adjusted_limit)
        adjusted_width = min(full_image_width * tolerance, adjusted_limit)

        # Convert the coordinates from percentages back to absolute coordinates
        best_match = (
            int(max(0, best_match_percent[0] * full_image_width - adjusted_width)),
            int(max(0, best_match_percent[1] * full_image_height - adjusted_high)),
        )
        bottom_right = (
            int(
                min(
                    full_image_width,
                    bottom_right_percent[0] * full_image_width + adjusted_width,
                )
            ),
            int(
                min(
                    full_image_height,
                    bottom_right_percent[1] * full_image_height + adjusted_high,
                )
            ),
        )

        matched_image = full_image[
            best_match[1] : bottom_right[1], best_match[0] : bottom_right[0]
        ]
        target_loc = get_target_loc(matched_image, self.image, self.threshold)
        return [(pt[0] + best_match[0], pt[1] + best_match[1]) for pt in target_loc]

    @staticmethod
    def __find_target_in_image(
        full_image_path: str, target_image_path: str
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        # Load the full image and the target image
        full_image = cv2.imread(full_image_path)
        target_image = cv2.imread(target_image_path)

        # Store the coordinates of the best match
        best_match = None
        best_val = float("inf")

        # Create an image pyramid for the full image
        pyramid = [full_image]
        while (
            pyramid[-1].shape[0] >= target_image.shape[0]
            and pyramid[-1].shape[1] >= target_image.shape[1]
        ):
            pyramid.append(cv2.pyrDown(pyramid[-1]))

        # Try to match the target image with each level of the pyramid
        for i, p in enumerate(pyramid):
            # Use template matching to find the target in the pyramid level
            result = cv2.matchTemplate(p, target_image, cv2.TM_SQDIFF_NORMED)

            # Find the location of the minimum value in the result
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # If the match is better than the best match so far, update the best match
            if min_val < best_val:
                best_val = min_val
                best_match = (min_loc[0] * (2**i), min_loc[1] * (2**i))

        # If no good matches found, return None
        if best_match is None:
            return None

        # Calculate the bottom right corner of the target image in the full image
        bottom_right = (
            best_match[0] + target_image.shape[1],
            best_match[1] + target_image.shape[0],
        )

        # Get the dimensions of the full image
        full_image_height, full_image_width = full_image.shape[:2]
        # Convert the coordinates to percentages
        best_match_percent = (
            best_match[0] / full_image_width,
            best_match[1] / full_image_height,
        )
        bottom_right_percent = (
            bottom_right[0] / full_image_width,
            bottom_right[1] / full_image_height,
        )

        return best_match_percent, bottom_right_percent
