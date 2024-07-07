import shutil
from random import randrange
from typing import Union

from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse, HTMLResponse
from starlette.staticfiles import StaticFiles

from photo import Photos

import http.server
import socketserver

# run --> uvicorn main:app --host 0.0.0.0 --port 8000
app = FastAPI()
app.mount("/.well-known", StaticFiles(directory="./.well-known"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/cluster")
def cluster(photos: Photos):
    num_group = max(2, randrange(int(len(photos.photos)/2)))
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


@app.post("/makeSticker")
async def make_sticker(file: UploadFile, with_border=False):
    temp_file_path = "temp.tmp"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return FileResponse(temp_file_path)


@app.get("/test")
def test():
    return {"hello": "world"}


@app.get("/deeplink")
def deeplink():
    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Open App</title>
            <script type="text/javascript">
                function openApp() {
                    var now = new Date().valueOf();
                    setTimeout(function () {
                        // Check if the app has opened or not after a delay
                        if (new Date().valueOf() - now > 100) {
                            // If app didn't open, redirect to the Google Play Store
                            window.location = "https://play.google.com/store/apps/details?id=com.leon.photo_cleaner";
                        }
                    }, 50);
                    
                    // Attempt to open the app using the custom URL scheme
                    window.location = "https://evolutionary-chiquita-leon-nguyen-b4118fcd/deeplink";
                }
            </script>
        </head>
        <body onload="openApp()">
            <p>Opening the app...</p>
        </body>
        </html>
        """
    return HTMLResponse(content=html_content)
