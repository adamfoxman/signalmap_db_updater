from models import Transmitter


class Reader:
    transmitter_list: list[Transmitter] = []

    def __init__(self, source=None, country: str = None):
        pass

    def get_transmitter_list(self):
        return self.transmitter_list