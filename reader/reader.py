from models.transmitter import Transmitter


class Reader:
    transmitter_list: list[Transmitter] = []

    def __init__(self, source):
        pass

    def import_data(self, source):
        pass

    def get_transmitter_list(self):
        return self.transmitter_list
