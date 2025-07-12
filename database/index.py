from typing import List


class Index:
    """
        Creates a sorted search structure used for querying
    """

    def __init__(self):
        raise NotImplementedError()

    def add_to_index(self, key: str, entry: dict):
        raise NotImplementedError()

    def remove_from_index(self, key: str):
        raise NotImplementedError()

    def search(self, key: str):
        raise NotImplementedError()

    def range_query(self, start: str, end: str) -> List:
        raise NotImplementedError()

    def starts_with(self, query_string: str):
        raise NotImplementedError()
