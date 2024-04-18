import unittest
from unittest.mock import patch, Mock
from controlled_module.src.serve import GUICatcherServiceServicer

serve_path = "controlled_module.src.serve"


class TestGUICatcherServiceServicer(unittest.TestCase):
    def setUp(self):
        self.servicer = GUICatcherServiceServicer()

    @patch(f"{serve_path}.screenshot", return_value=(b"image", (0, 0)))
    def test_ScreenShot(self, mock_screenshot):
        request = Mock()
        request.window_name = "test_window"
        context = Mock()
        response = self.servicer.ScreenShot(request, context)
        mock_screenshot.assert_called_once_with("test_window")
        self.assertEqual(response.image, b"image")
        self.assertEqual(response.left_top_x, 0)
        self.assertEqual(response.left_top_y, 0)

    @patch(f"{serve_path}.keyboard.press")
    def test_KeyboardEvent(self, mock_press):
        request = Mock()
        request.key = "test_key"
        request.action = "test_action"
        context = Mock()
        self.servicer.KeyboardEvent(request, context)
        mock_press.assert_called_once_with("test_key", "test_action")

    @patch(f"{serve_path}.mouse.action")
    def test_MouseEvent(self, mock_action):
        request = Mock()
        request.action = "test_action"
        request.x = 0
        request.y = 0
        request.button = "test_button"
        request.interval = 0
        request.over_time = 0
        request.length = 0
        request.direction = "test_direction"
        context = Mock()
        self.servicer.MouseEvent(request, context)
        mock_action.assert_called_once_with(
            "test_action", 0, 0, "test_button", 0, 0, 0, "test_direction"
        )

    @patch(f"{serve_path}.run_command", return_value=(0, "stdout", "stderr"))
    def test_RunCommand(self, mock_run_command):
        request = Mock()
        request.command = "test_command"
        context = Mock()
        response = self.servicer.RunCommand(request, context)
        mock_run_command.assert_called_once_with("test_command")
        self.assertEqual(response.exit_code, 0)
        self.assertEqual(response.stdout, "stdout")
        self.assertEqual(response.stderr, "stderr")


if __name__ == "__main__":
    unittest.main()
