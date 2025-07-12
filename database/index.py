from typing import List


class Index:
    """
        Creates a sorted search structure used for querying
    """

    def __init__(self):
        self.keys = []

    def add_to_index(self, key: str):
        self.keys.append(key)
        self.keys = sorted(self.keys)

    def remove_from_index(self, key: str):
        self.keys.remove(key)

    def search(self, key: str):
        if key in self.keys:
            return key

    def range_query(self, start: str, end: str) -> List:
        raise NotImplementedError()

    def starts_with(self, query_string: str):
        raise NotImplementedError()
