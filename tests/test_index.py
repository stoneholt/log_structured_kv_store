import pytest

from database.index import Index


def test_basic_index():
    idx = Index()
    idx.add_to_index(4)
    idx.add_to_index(5)

    assert idx.search(4) == 4
    assert idx.search(5) == 5
    assert idx.search(6) == None

    idx.remove_from_index(5)
    assert idx.search(5) == None


def test_index_with_strings():
    idx = Index()
    idx.add_to_index("apple")
    idx.add_to_index("banana")
    idx.add_to_index("cheese")
    idx.add_to_index("dog")

    assert idx.search("cheese") == "cheese"


def test_index_with_strings():
    idx = Index()
    idx.add_to_index("apple")
    idx.add_to_index("banana")
    idx.add_to_index("cheese")
    idx.add_to_index("dog")
    idx.keylist.display()
    assert 1 == 2
