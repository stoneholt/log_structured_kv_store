from database.keydir import KeyDir
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

def test_insert():
    with patch("database.keydir.KeyDir._validate_folder", mock_open()):
        kd = KeyDir()
        kd._write_to_file = MagicMock(return_value=["file_id", 0])
        kd.insert("test_key", "test_value")

    expected = {"test_key": {"file_id": "file_id", "value_position": 0}}
    assert kd.dir == expected

def test_find_value_none():
    kd = KeyDir()
    value = kd.find_value("fake_key")

    assert value == None

def test_find_value_exists():
    kd = KeyDir()
    kd.insert("test_key", "test_value")
    value = kd.find_value("test_key")

    assert value == "test_value"