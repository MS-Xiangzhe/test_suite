import time
import cv2
import re
import numpy as np
from pathlib import Path

video_path = "C:\\Users\\v-xceng\\Videos\\rec.mp4"
target_img_directory = "D:\\test\\img"
select_frame = 2


result_img_directory = "D:\\test\\result"
result_img_directory_path = Path(result_img_directory)
result_img_directory_path.mkdir(parents=True, exist_ok=True)


def get_target_loc(image, target_image, threshold=0.7) -> list[tuple[int, int]]:
    res = cv2.matchTemplate(image, target_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return list(zip(*loc[::-1]))


def check_target_image_exist_in_image(image, target_image) -> bool:
    loc = get_target_loc(image, target_image)
    for pt in zip(*loc[::-1]):
        w, h, _ = target_image.shape
        cv2.rectangle(image, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)
        cv2.imwrite(str((result_img_directory_path / f"{time.time()}.png")), image)
        return True
    return False


def draw_frames_and_save(full_image, target_image, coordinates_percent, output_path):
    # Get the dimensions of the full image
    full_image_height, full_image_width = full_image.shape[:2]

    for pt_percent in coordinates_percent:
        # Convert the coordinates from percentages back to absolute coordinates
        pt = (
            int(pt_percent[0] * full_image_width),
            int(pt_percent[1] * full_image_height),
        )
        w, h = target_image.shape[::2]
        bottom_right = (pt[0] + h, pt[1] + w)
        cv2.rectangle(full_image, pt, bottom_right, (0, 0, 255), 2)
    cv2.imwrite(output_path, full_image)


def parse_file_name(file_name: str) -> list[str]:
    file_name = Path(file_name).with_suffix("").name
    i = int(re.search(r"\d+", file_name).group())
    return [str(i)] + file_name[len(str(i)) :].split("_")


def test_parse_file_name():
    assert parse_file_name("1start.png") == ["1", "start"]
    assert parse_file_name("1111end.png") == ["1111", "end"]
    assert parse_file_name("1start_from.png") == ["1", "start", "from"]
    assert parse_file_name("1111end_to_0.7.png") == ["1111", "end", "to", "0.7"]


def get_time_length_by_key_time_list(
    key_dict: dict[str, str], key_time_list: list[tuple[str, float]]
) -> list[tuple[str, float, float]]:
    start_key_list = list(key_dict.keys())
    end_key_list = list(key_dict.values())
    key_dict_reverse = {value: key for key, value in key_dict.items()}

    baned_key_map: dict[str, str] = {}
    tmp_time_map: dict[str, float] = {}

    time_dict: dict[tuple[str, float], float] = {}  # (start_key, start_time, span)

    for file_name, key_time in key_time_list:
        if file_name in baned_key_map:
            continue
        unban_key_list = []
        if file_name in baned_key_map.values():
            for key, value in baned_key_map.items():
                if value == file_name:
                    unban_key_list.append(key)
        for key in unban_key_list:
            baned_key_map.pop(key)

        *_, from_or_to = parse_file_name(file_name)
        if from_or_to == "from":
            if file_name in start_key_list:
                baned_key_map[file_name] = key_dict[file_name]
            elif file_name in end_key_list:
                baned_key_map[file_name] = key_dict_reverse[file_name]

        if file_name in start_key_list:
            tmp_time_map[file_name] = key_time
        elif file_name in end_key_list:
            start_key = key_dict_reverse[file_name]
            try:
                start_time = tmp_time_map[start_key]
            except KeyError:
                start_time = None
            if start_time:
                span = key_time - start_time
                time_dict[(start_key, start_time)] = span
    return [(key, start_time, span) for (key, start_time), span in time_dict.items()]


def test_get_time_length_by_key_time_list():
    key_dict = {"1start.png": "1end.png", "2start.png": "2end.png"}
    key_time_list = [
        ("1start.png", 1),
        ("1end.png", 2),
        ("2start.png", 3),
        ("2end.png", 4),
    ]
    time_list = get_time_length_by_key_time_list(key_dict, key_time_list)
    assert time_list == [("1start.png", 1, 1), ("2start.png", 3, 1)]

    key_dict = {"1start_from.png": "1end.png", "2start_to.png": "2end.png"}
    key_time_list = [
        ("1start_from.png", 1),
        ("1start_from.png", 1.1),
        ("1end.png", 2),
        ("2start_to.png", 3),
        ("2start_to.png", 3.1),
        ("2end.png", 4),
    ]
    time_list = get_time_length_by_key_time_list(key_dict, key_time_list)
    assert time_list == [("1start_from.png", 1, 1), ("2start_to.png", 3.1, 4 - 3.1)]

    key_dict = {"1start.png": "1end_from.png", "2start.png": "2end_to.png"}
    key_time_list = [
        ("1start.png", 1),
        ("1end_from.png", 2),
        ("1end_from.png", 2.1),
        ("2start.png", 3),
        ("2end_to.png", 4),
        ("2end_to.png", 4.1),
    ]
    time_list = get_time_length_by_key_time_list(key_dict, key_time_list)
    assert time_list == [("1start.png", 1, 1), ("2start.png", 3, 4.1 - 3)]

    key_dict = {"1start_from.png": "1end_from.png", "2start_to.png": "2end_to.png"}
    key_time_list = [
        ("1start_from.png", 1),
        ("1end_from.png", 2),
        ("1end_from.png", 2.1),
        ("2start_to.png", 3),
        ("2start_to.png", 3.1),
        ("1start_from.png", 3.1),
        ("2end_to.png", 4),
        ("2end_to.png", 4.1),
        ("1end_from.png", 4.2),
    ]
    time_list = get_time_length_by_key_time_list(key_dict, key_time_list)
    assert time_list == [
        ("1start_from.png", 1, 1),
        ("2start_to.png", 3.1, 4.1 - 3.1),
        ("1start_from.png", 3.1, 4.2 - 3.1),
    ]


class TargetImage:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.threshold = 0.7
        args = parse_file_name(path)
        if len(args) >= 3:
            from_or_to = args[2]
            self.stop_at_begin = from_or_to == "from"
            if len(args) >= 4:
                try:
                    self.threshold = float(args[-1])
                except Exception:
                    pass
        self.image = cv2.imread(str(path))
        self.split_coordinate = None

    def init_split_coordinate(self, full_image_path: str):
        self.split_coordinate = self.__find_target_in_image(
            full_image_path, str(self.path)
        )
        if self.split_coordinate is None:
            raise Exception(f"Can't find {self.path} in {full_image_path}")

    def test_split_coordinate(self, full_image_path: str):
        full_image = cv2.imread(full_image_path)
        coordinate_list = self.get_coordinate_list_in_full_image(full_image)
        if not coordinate_list:
            raise Exception(f"Can't find {self.path} in {full_image_path}")
        full_image = cv2.imread(full_image_path)
        rsl_path = add_suffix_to_filename(
            str(result_img_directory_path / self.path.name), f"full{time.time()}"
        )
        draw_frames_and_save(full_image, self.image, coordinate_list, rsl_path)

    def get_coordinate_list_in_full_image(
        self, full_image: str
    ) -> tuple[(tuple[int, int], tuple[int, int])]:
        tolerance = 0.1
        best_match_percent, bottom_right_percent = self.split_coordinate

        # Get the dimensions of the full image
        full_image_height, full_image_width = full_image.shape[:2]

        # Convert the coordinates from percentages back to absolute coordinates
        best_match = (
            max(0, int((best_match_percent[0] - tolerance) * full_image_width)),
            max(0, int((best_match_percent[1] - tolerance) * full_image_height)),
        )
        bottom_right = (
            min(
                full_image_width,
                int((bottom_right_percent[0] + tolerance) * full_image_width),
            ),
            min(
                full_image_height,
                int((bottom_right_percent[1] + tolerance) * full_image_height),
            ),
        )

        matched_image = full_image[
            best_match[1] : bottom_right[1], best_match[0] : bottom_right[0]
        ]
        return get_target_loc(matched_image, self.image, self.threshold)

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


def add_suffix_to_filename(filename: str, suffix: str) -> str:
    # Create a Path object from the filename
    path = Path(filename)
    # Add the suffix to the stem (the file name without the extension)
    new_stem = f"{path.stem}_{suffix}"
    # Combine the new stem with the extension
    new_filename = path.with_stem(new_stem)
    return str(new_filename)


def test_add_suffix_to_filename():
    assert add_suffix_to_filename("test.txt", "suffix") == "test_suffix.txt"
    assert add_suffix_to_filename("test", "suffix") == "test_suffix"
    assert add_suffix_to_filename("test.txt", "") == "test_.txt"


def get_img_dict(img_dir):
    text_dict = {}
    target_img_directory = Path(img_dir)
    for file in Path(target_img_directory).iterdir():
        if file.is_file():
            file_path = str(file)
            args = parse_file_name(file_path)
            if args[-1] == "full":
                continue
            i, start_prefix, *_ = args
            text_cell = text_dict.setdefault(i, [None, None])
            if start_prefix == "start":
                text_cell[0] = file_path
            elif start_prefix == "end":
                text_cell[1] = file_path

    image_dict = {}
    for i in text_dict.keys():
        if text_dict[i][0] is None or text_dict[i][1] is None:
            raise Exception(f"Can't find start or end for {i}")
        start_image_path = text_dict[i][0]
        start_image = TargetImage(start_image_path)
        start_image_full_path = add_suffix_to_filename(start_image_path, "full")
        start_image.init_split_coordinate(start_image_full_path)
        start_image.test_split_coordinate(start_image_full_path)
        end_image_path = text_dict[i][1]
        end_image = TargetImage(end_image_path)
        end_image_full_path = add_suffix_to_filename(end_image_path, "full")
        end_image.init_split_coordinate(end_image_full_path)
        end_image.test_split_coordinate(end_image_full_path)
        image_dict[start_image] = end_image
    return image_dict


def main(
    video_path: str, image_dict: dict[TargetImage, TargetImage], select_frame: int = 1
):
    start_image_map = {image.path: image for image in image_dict.keys()}
    end_image_map = {image.path: image for image in image_dict.values()}

    key_time_list: list[tuple[str, float]] = []

    vidcap = cv2.VideoCapture(video_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    total_frame = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("fps:", fps, "select_fps:", fps / select_frame)
    frames_count = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if not success:
            break
        frames_count += 1
        print(frames_count, "/", total_frame)
        if select_frame > 0:
            if frames_count % select_frame != 0:
                continue
        pass_index_list = []
        for index, (image_path, target_image) in enumerate(start_image_map.items()):
            if target_image.get_coordinate_list_in_full_image(image):
                video_time = frames_count / fps
                key_time_list.append((image_path, video_time))
                print("select_frame:", frames_count)
                pass_index_list.append(index)
        for index, (image_path, target_image) in enumerate(end_image_map.items()):
            if index in pass_index_list:
                continue
            if target_image.get_coordinate_list_in_full_image(image):
                video_time = frames_count / fps
                key_time_list.append((image_path, video_time))
                print("select_frame:", select_frame)

    print(key_time_list)
    image_path_dict = {
        start_image.path: end_image.path
        for start_image, end_image in image_dict.items()
    }
    time_list = get_time_length_by_key_time_list(image_path_dict, key_time_list)
    return time_list


if __name__ == "__main__":
    text_dict = get_img_dict(target_img_directory)
    print(video_path)
    print(text_dict)
    time_dict = main(video_path, text_dict, select_frame)
    print(time_dict)
