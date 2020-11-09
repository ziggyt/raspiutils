from datetime import datetime

from picamera import PiCamera  # will always throw error if not on raspberry pi


class CameraModule():

    def __init__(self, path: str):
        self.camera = PiCamera()
        self.path = path

    def take_picture(self):
        now = datetime.now()
        date_time_string = now.strftime("%m/%d/%Y, %H:%M:%S")

        file_path = f'{self.path}{date_time_string}.jpg'
        self.camera.capture(file_path)
        print(f"Took picture {file_path}")
