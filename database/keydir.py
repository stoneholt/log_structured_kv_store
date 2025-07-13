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
        timestamp = time()
        self.active_file = f"{timestamp}-data.dat"
        with Path.open(Path(f"./data/{self.active_file}"), "ab") as f:
            for key in self.dir:
                value = self.find_value(key)
                position = f.tell()
                encoded_key = key.encode("utf-8")
                key_size = len(encoded_key).to_bytes(4, "big")
                f.write(key_size)
                encoded_value = value.encode("utf-8")
                value_size = len(encoded_value).to_bytes(4, "big")
                f.write(value_size)
                f.write(encoded_key)
                f.write(encoded_value)
                self.dir[key]["file_id"] = self.active_file
                self.dir[key]["position"] = position
            f.flush()

        for file in Path("./data").iterdir():
            if file != self.active_file:
                file.unlink()

    def _validate_file(self):
        if self.active_file == "":
            timestamp = time()
            self.active_file = f"{timestamp}-data.dat"
        elif (Path(f"./data/{self.active_file}").stat().st_size / (1024 * 1024 * 1024)) > 2: # file bigger than 2 GB (or whatever value)
            if len(Path("./data").iterdir()) > 10: # more than 10 files used
                self._clean_data_directory()
            timestamp = time()
            self.active_file = f"{timestamp}-data.dat"

    def _write_to_file(self, key: str, value: str) -> list[str, int]:
        # needs to return file ID, value size, value position, and timestamp
        self._validate_folder()
        self._validate_file()
        with Path.open(Path(f"./data/{self.active_file}"), "ab") as f:
            position = f.tell()
            encoded_key = key.encode("utf-8")
            key_size = len(encoded_key).to_bytes(4, "big")
            f.write(key_size)
            encoded_value = value.encode("utf-8")
            value_size = len(encoded_value).to_bytes(4, "big")
            f.write(value_size)
            f.write(encoded_key)
            f.write(encoded_value)
            f.flush()

        return [self.active_file, position]

    def insert(self, key: str, value: str) -> None:
        file_id, position = self._write_to_file(key, value)
        self.dir[key] = { "file_id": file_id, "position": position }
        self.keys.add_to_index(key)

    def delete(self, key: str) -> None:
        if key in self.dir[key]:
            del self.dir[key]
            self._write_to_file(key, DELETE_MARKER)

    def find_value(self, key: str) -> str | None:
        if key in self.dir:
            file_id, value_position = self.dir[key]["file_id"], self.dir[key]["value_position"]
            with Path.open(Path(f"./data/{file_id}"), "rb") as f:
                f.seek(value_position)
                key_size = f.read(4)
                value_size = f.read(4)
                f.seek(int.from_bytes(key_size, "big"), 1)
                decoded_value = f.read(int.from_bytes(value_size, "big")).decode("utf-8")
                return decoded_value

        return None
