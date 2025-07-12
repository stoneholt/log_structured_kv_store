from fastapi import FastAPI
from .index import Index
from .keydir import KeyDir
from pydantic import BaseModel

from abc import ABC, abstractmethod

from fastapi import FastAPI

app = FastAPI()


class DataStore(ABC):
    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def prefix_query(self, query):
        pass


class KVStore(DataStore):
    def __init__(self):
        self.db = KeyDir()

    def get(self, key):
        return self.db.find_value(key)

    def put(self, key, value):
        self.db.insert(key, value)

    def delete(self, key):
        self.db.delete(key)

    def prefix_search(self, query):
        return self.db.prefix_search(query)


class SimpleDataStore(DataStore):
    def __init__(self):
        self.data = {}
        self.index = Index()
        pass

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None

    def put(self, key, value):
        self.index.add_to_index(key)
        self.data[key] = value

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.index.remove_from_index(key)

    def prefix_search(self, query):
        keys = self.index.starts_with(query)
        results = []
        for key in keys:
            results.append((key, self.data[key]))
        return results


class Payload(BaseModel):
    data: str


store = SimpleDataStore()


@app.get("/v1/{key}")
def get_key(key: str):

    return {"data": store.get(key)}


@app.put("/v1/{key}")
def put_key(key: str, body: Payload):
    store.put(key, body.data)
    return {"data": {"key": key, "body": body.data}}


@app.delete("/v1/{key}")
def delete_key(key: str):
    store.delete(key)
    return {"data": "deleted"}


@app.get("/v1/prefix/{prefix}")
def prefix_search(prefix: str):
    results = store.prefix_search(prefix)
    return {"data": results}
