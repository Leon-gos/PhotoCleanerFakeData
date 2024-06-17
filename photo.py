from pydantic import BaseModel


class Photo(BaseModel):
    name: str
    feature: list[float]


class Photos(BaseModel):
    photos: list[Photo]
