
# TODO: implement this mock object
class Detector:
    def __init__(self):
        self.activated = False

    def start(self) -> None:
        self.activated = True

    def stop(self) -> None:
        self.activated = False

    def eye_opened(self) -> bool:
        return false

    def eye_closed(self) -> bool:
        return not self.eye_opened()