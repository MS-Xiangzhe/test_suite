from .get_runtime_from_rec_by_img import (
    get_time_length_by_key_time_list,
    add_suffix_to_filename,
)


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
