import shutil
from random import randrange
from typing import Union

from fastapi import FastAPI, UploadFile, Request
from starlette.responses import FileResponse, HTMLResponse, JSONResponse
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


@app.get("/deeplink/{path:path}", response_class=HTMLResponse)
async def redirect_to_app_or_store(path: str, request: Request):
    user_agent = request.headers.get("user-agent", "").lower()
    is_android = "android" in user_agent

    # Replace with your actual URLs
    android_app_url = (f"intent://evolutionary-chiquita-leon-nguyen-b4118fcd.koyeb.app/deeplink/{path}#Intent;"
                       "scheme=https;"
                       "package=com.leon.photo_cleaner;"
                       "end")
    android_store_url = "https://play.google.com/store/apps/details?id=com.leon.photo_cleaner"

    if is_android:
        print("android")
        # Redirect to Android app or Play Store
        return HTMLResponse(f"""
            <html>
            <head>
                <title>Redirecting...</title>
                <meta http-equiv="refresh" content="0; url={android_app_url}">
                <script>
                    setTimeout(function() {{
                        window.location.href = "{android_store_url}";
                    }}, 3000);
                </script>
            </head>
            <body>
                <p>If you are not redirected, <a href="{android_store_url}">click here</a>.</p>
            </body>
            </html>
        """)
    else:
        print("default")
        # Default fallback
        return HTMLResponse(f"""
            <html>
            <head>
                <title>Redirecting...</title>
            </head>
            <body>
                <p>Unsupported device. Please use an Android or iOS device.</p>
            </body>
            </html>
        """)

