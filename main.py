from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: str = True
    ratings: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "These are my posts!"}


@app.post("/posts")
def create_post(post: Post):
    print(post)
    return {"data": "new post"}
