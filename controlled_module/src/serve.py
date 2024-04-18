from concurrent import futures
import grpc
from proto import api_pb2, api_pb2_grpc
from google.protobuf.empty_pb2 import Empty

from .gui_catcher.screenshot import screenshot
from .gui_operator import keyboard
from .gui_operator import mouse
from .command_runner.command import run_command


class GUICatcherServiceServicer(api_pb2_grpc.GUICatcherServiceServicer):
    def ScreenShot(self, request, context):
        window_name = request.window_name
        try:
            image, left_top = screenshot(window_name)
            return api_pb2.ScreenShotResponse(
                image=image, left_top_x=left_top[0], left_top_y=left_top[1]
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return api_pb2.ScreenShotResponse(image=b"", left_top_x=-1, left_top_y=-1)

    def KeyboardEvent(self, request, context):
        keys = request.keys
        action = request.action
        action = keyboard.PressStatus.str_to_enum(action)
        try:
            keyboard.press(keys, action)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
        return Empty()

    def KeyboardInput(self, request, context):
        text = request.text
        interval = request.interval
        try:
            keyboard.input(text, interval)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
        return Empty()

    def MouseEvent(self, request, context):
        action = request.action
        action = mouse.MouseAction.str_to_enum(action)
        x = request.x
        y = request.y
        button = request.button
        interval = request.interval
        over_time = request.over_time
        length = request.length
        direction = request.direction

        try:
            mouse.action(action, x, y, button, interval, over_time, length, direction)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
        return Empty()

    def RunCommand(self, request, context):
        command = request.command
        try:
            exit_code, stdout, stderr = run_command(command)
            return api_pb2.RunCommandResponse(
                exit_code=exit_code, stdout=stdout, stderr=stderr
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return api_pb2.RunCommandResponse(result="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_GUICatcherServiceServicer_to_server(
        GUICatcherServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
