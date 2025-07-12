from database.index import Index


def test_basic_index():
    idx = Index()
    idx.add_to_index(4)
    idx.add_to_index(5)

    assert 4 == idx.search(4)
    assert 5 == idx.search(5)
    assert None == idx.search(6)

    idx.remove_from_index(5)
    assert None == idx.search(5)


def test_index_with_strings():
    idx = Index()
    idx.add_to_index("apple")
    idx.add_to_index("banana")
    idx.add_to_index("cheese")
    idx.add_to_index("dog")

    assert "cheese" == idx.search("cheese")


def test_prefix_search():
    idx = Index()
    idx.add_to_index("alfred")
    idx.add_to_index("cheese")
    idx.add_to_index("cheddar")
    idx.add_to_index("chew")
    idx.add_to_index("abchew")
    idx.add_to_index("dog")
    idx.add_to_index("zebra")
    idx.add_to_index("cha")

    assert ["cheddar", "cheese", "chew"] == idx.starts_with("che")
