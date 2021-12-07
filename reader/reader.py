from models import Transmitter


class Reader:
    """
    This class is used to read the data from the database. It's used by the ExternalReader class.
    """
    transmitter_list: list[Transmitter] = []

    def __init__(self, source=None, country: str = None):
        pass

    def get_transmitter_list(self):
        return self.transmitter_list
