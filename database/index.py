from .skiplist import SkipList


class Index:
    """
        Creates a sorted search structure used for querying
    """

    def __init__(self):
        self.keylist = SkipList()

    def add_to_index(self, key: str):
        self.keylist.insert(key)

    def remove_from_index(self, key: str):
        self.keylist.delete(key)

    def search(self, key: str):
        return self.keylist.search(key)

    def range_query(self, start: str, end: str) -> list:
        raise NotImplementedError()

    def starts_with(self, query_string: str) -> list:
        return self.keylist.starts_with(query_string)
