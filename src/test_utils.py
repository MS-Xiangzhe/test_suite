from utils import parse_file_name, add_suffix_to_filename


def test_parse_file_name():
    assert parse_file_name("1_start.png") == [1, "start"]
    assert parse_file_name("1111_end.png") == [1111, "end"]
    assert parse_file_name("1_start_from.png") == [1, "start", "from"]
    assert parse_file_name("1111_end_to_0.7.png") == [1111, "end", "to", "0.7"]
    assert parse_file_name("1111_222_123_end_to_0.7.png") == [
        1111,
        222,
        123,
        "end",
        "to",
        "0.7",
    ]


def test_add_suffix_to_filename():
    assert add_suffix_to_filename("test.txt", "suffix") == "test_suffix.txt"
    assert add_suffix_to_filename("test", "suffix") == "test_suffix"
    assert add_suffix_to_filename("test.txt", "") == "test_.txt"
