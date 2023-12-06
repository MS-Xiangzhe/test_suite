import time
import cv2
from pathlib import Path
from target_image import TargetImage
from utils import parse_file_name, add_suffix_to_filename
from cv2utils import draw_frames_and_save

VIDEO_PATH = "C:\\Users\\v-xceng\\Videos\\rec.mp4"
TARGET_IMG_DIR = "D:\\test\\img"
SELECT_FRAME = 2


RESULT_IMG_DIR = "D:\\test\\result"
RESULT_IMG_DIR_PATH = Path(RESULT_IMG_DIR)
RESULT_IMG_DIR_PATH.mkdir(parents=True, exist_ok=True)


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


def get_img_dict(img_dir):
    image_path_dict = {}
    target_img_directory = Path(img_dir)
    for file in Path(target_img_directory).iterdir():
        if file.is_file():
            image = TargetImage(file)
            if image.is_full:
                continue
            i = image.index_list[0]
            sub_index = image.index_list[1]
            text_cell = image_path_dict.setdefault(i, {})
            text_cell[sub_index] = image

    image_dict = {}
    for i in image_path_dict.keys():
        if image_path_dict[i][1] is None or image_path_dict[i][2] is None:
            raise Exception(f"Can't find start or end for {i}")
        start_image = image_path_dict[i][1]
        start_image_full_path = add_suffix_to_filename(start_image.path, "full")
        start_image.init_split_coordinate(start_image_full_path)
        start_image.test_split_coordinate(start_image_full_path)
        end_image = image_path_dict[i][2]
        end_image_full_path = add_suffix_to_filename(end_image.path, "full")
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
        for map in [start_image_map, end_image_map]:
            for image_path, target_image in map.items():
                coordinate_list = target_image.get_coordinate_list_in_full_image(image)
                if coordinate_list:
                    rsl_path = str(
                        RESULT_IMG_DIR_PATH
                        / image_path.with_stem(f"{time.time()}_{image_path.stem}").name
                    )
                    draw_frames_and_save(
                        image, target_image.image, coordinate_list, rsl_path
                    )
                    video_time = frames_count / fps
                    key_time_list.append((image_path, video_time))
                    print("selected_frame:", frames_count, "video_time:", video_time)
    print(key_time_list)
    image_path_dict = {
        start_image.path: end_image.path
        for start_image, end_image in image_dict.items()
    }
    time_list = get_time_length_by_key_time_list(image_path_dict, key_time_list)
    return time_list


if __name__ == "__main__":
    img_dict = get_img_dict(TARGET_IMG_DIR)
    print(VIDEO_PATH)
    print(img_dict)
    time_dict = main(VIDEO_PATH, img_dict, SELECT_FRAME)
    print(time_dict)
