from models.transmitter import Transmitter


class Reader(type):
    transmitter_list: list[Transmitter] = []

    def import_data(self, source):
        pass

    def get_transmitter_list(self):
        return self.transmitter_list
