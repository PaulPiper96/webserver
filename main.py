from fastapi import FastAPI
from typing import List

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    # 'skip' and 'limit' become query params: ?skip=...&limit=...
    return fake_items_db[skip : skip + limit]
    # Return a slice of the fake DB list using skip and limit values


@app.get("/items/{item_id}")
async def read_item(item_id: int | None = None):
    if item_id:
        return fake_items_db[item_id]




@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"hello": "fastapi"}

