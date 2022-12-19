from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "These are my posts!"}


@app.post("/posts")
def create_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": "Created your post!"}
