
class Index:
    def __init__(self):
        raise NotImplementedError()

    def add_to_index(self, key: str, entry: dict):
        raise NotImplementedError()

    def remove_from_index(self, key: str):
        raise NotImplementedError()
