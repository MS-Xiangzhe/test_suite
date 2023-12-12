from target_image import TargetImage


def test_init_target_image():
    target_image = TargetImage("1_1_提示这里是开始_from_full.png")
    assert target_image.index_list == [1, 1]
    assert target_image.stop_at_begin is True
    assert target_image.is_full is True
