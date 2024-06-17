import shutil
from random import randrange
from typing import Union

from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse

from photo import Photos

# run --> uvicorn main:app --host 0.0.0.0 --port 8000
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/cluster")
def cluster(photos: Photos):
    num_group = min(2, randrange(int(len(photos.photos)/2)))
    groups = {}

    for i in range(num_group):
        groups[i] = []

    for i in range(len(photos.photos)):
        groups[i % num_group].append(photos.photos[i].name)

    return {"groups": groups}
    # return {
    #     "list_length": len(photos.photos)
    # }


@app.post("/enhanceResolution")
async def enhance_resolution(file: UploadFile):
    temp_file_path = "temp.tmp"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return FileResponse(temp_file_path)


@app.post("/assessmentQuality")
def assessment_quality(files: list[UploadFile]):
    rank = {}
    for i in range(len(files)):
        rank[files[i].filename] = i + 1
    return rank


@app.get("/test")
def test():
    return {"hello": "world"}
