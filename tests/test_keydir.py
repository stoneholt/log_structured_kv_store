from database.keydir import KeyDir
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

def test_keydir():

    with patch("database.keydir.KeyDir._validate_folder", mock_open()):
        kd = KeyDir()
        kd._write_to_file = MagicMock(return_value=["file_id", 0, 0, 0.0])
        kd.insert("test_key", "test_value")

    expected = {"test_key": {"file_id": "file_id", "value_size": 0, "value_position": 0, "timestamp": 0.0}}
    assert kd.dir == expected