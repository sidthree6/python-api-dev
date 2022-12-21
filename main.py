from typing import Optional
from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: str = True
    ratings: Optional[int] = None

my_posts = [
    {
        "title": "My first post 1",
        "content": "Content of post 1",
        "id": 1
    },
    {
        "title": "My first post 2",
        "content": "Content of post 2",
        "id": 2
    }
]


def find_post_by_id(id: int):
    for post in my_posts:
        if post.get("id") == id:
            return post
    return None


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post_by_id(id)
    if not post:
        response.status_code = 404
    return {"data": post}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
