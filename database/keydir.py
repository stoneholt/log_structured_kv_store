from database.index import Index
from time import time
from pathlib import Path

DELETE_MARKER = "t0MbStoNe"


class KeyDir:
    dir: dict = {}
    keys: Index = Index()
    active_file: str = ""

    def _validate_folder(self):
        if not Path("./data").is_dir():
            Path.mkdir("./data")

    def _clean_data_directory(self):
        pass

    def _validate_file(self):
        if self.active_file == "":
            timestamp = time()
            self.active_file = f"{timestamp}-data.txt"
        elif (Path(f"./data/{self.active_file}").stat().st_size / (1024 * 1024 * 1024)) > 2: # file bigger than 2 GB (or whatever value)
            timestamp = time()
            self.active_file = f"{timestamp}-data.txt"
            if len(Path("./data").iterdir()) > 10: # more than 10 files used
                self._clean_data_directory()

    def _write_to_file(self, key: str, value: str) -> list[str, int, int, float]:
        # needs to return file ID, value size, value position, and timestamp
        self._validate_folder()
        self._validate_file()
        with Path.open(Path(f"./data/{self.active_file}"), "ab") as f:
            timestamp = time()
            encoded_key = key.encode("utf-8")
            key_size = len(encoded_key).to_bytes(4, "big")
            encoded_value = value.encode("utf-8")
            value_size = len(encoded_value).to_bytes(4, "big")
            entry = f"{timestamp}-{key_size}-{value_size}-{key}-{value}".encode("utf-8")
            position = f.tell()
            f.write(entry)
            f.flush()

        return [self.active_file, value_size, position, timestamp]

    def insert(self, key: str, value: str) -> None:
        file_id, value_size, value_position, timestamp = self._write_to_file(key, value)
        self.dir[key] = { "file_id": file_id, "value_size": value_size, "value_position": value_position, "timestamp": timestamp }
        self.keys.add_to_index(key)

    def delete(self, key: str) -> None:
        if key in self.dir[key]:
            del self.dir[key]
            self._write_to_file(key, DELETE_MARKER)
