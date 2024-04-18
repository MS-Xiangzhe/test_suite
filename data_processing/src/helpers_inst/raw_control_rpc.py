import grpc
from proto import api_pb2, api_pb2_grpc
from typing import Union
from PIL import Image
import numpy as np
import io
from ..config import RPC_SERVER_ADDRESS
from controlled_module.src.gui_operator.keyboard import PressStatus
from controlled_module.src.gui_operator.mouse import MouseAction


class GUICatcherClient:
    def __init__(self, server_address=RPC_SERVER_ADDRESS):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = api_pb2_grpc.GUICatcherServiceStub(self.channel)

    def screenshot(self, window_name: Union[str, None] = None):
        response = self.stub.ScreenShot(
            api_pb2.ScreenShotRequest(window_name=window_name)
        )
        return response

    def keyboard_event(self, keys, action):
        self.stub.KeyboardEvent(api_pb2.KeyboardEventRequest(keys=keys, action=action))

    def mouse_event(self, action, x, y, button, interval, over_time, length, direction):
        self.stub.MouseEvent(
            api_pb2.MouseEventRequest(
                action=action,
                x=x,
                y=y,
                button=button,
                interval=interval,
                over_time=over_time,
                length=length,
                direction=direction,
            )
        )

    def run_command(self, command):
        response = self.stub.RunCommand(api_pb2.RunCommandRequest(command=command))
        return response


client = GUICatcherClient()


def screenshot(
    window_name: Union[str, None] = None
) -> tuple[Image.Image, tuple[int, int]]:
    response = GUICatcherClient().screenshot(window_name)
    image_bytes = response.image
    image_bytes = np.array(Image.open(io.BytesIO(image_bytes)))
    left_top = (response.left_top_x, response.left_top_y)
    image = Image.fromarray(image_bytes)
    return image, left_top


def keyboard_event(keys: list[str], action: PressStatus):
    GUICatcherClient().keyboard_event(keys, str(action))


def mouse_event(
    action: MouseAction,
    x: int,
    y: int,
    button: str,
    interval: int,
    over_time: int,
    length: int,
    direction: str,
):
    GUICatcherClient().mouse_event(
        action, x, y, button, interval, over_time, length, direction
    )


def run_command(command) -> tuple[int, str, str]:
    response = GUICatcherClient().run_command(command)
    exit_code = response.exit_code
    stdout = response.stdout
    stderr = response.stderr
    return exit_code, stdout, stderr
