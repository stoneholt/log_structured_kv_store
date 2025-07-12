from fastapi import FastAPI
# from .keydir import KeyDir
from pydantic import BaseModel
app = FastAPI()


class Payload(BaseModel):
    data: str


@app.get("/v1/{key}")
def get_key(key: str):
    return {"message": "placeholder"}


@app.put("/v1/{key}")
def put_key(key: str, body: Payload):
    return {"message": "payload"}


@app.delete("/v1/{key}")
def delete_key(key: str):
    return {"message": "delete"}


@app.get("/v1/prefix/{prefix}")
def prefix_search(prefix: str):
    return {"message": "prefix"}
