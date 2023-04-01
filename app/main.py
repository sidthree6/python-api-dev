import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str
    published: str = True
    ratings: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post():
    cur.execute("""SELECT * FROM posts ORDER BY pid DESC LIMIT 1""")
    post = cur.fetchone()
    return {"data": post}


@app.post("/posts")
def create_post(post: Post):
    cur.execute("""INSERT INTO posts (title, content, published)
      VALUES (%s, %s, %s) RETURNING *""",
                (post.title, post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}


@ app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE pid = %s;""", (id,))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"data": post}


@ app.delete("/posts/{id}")
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE pid = %s RETURNING *;""", (id,))
    deleted_post = cur.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE pid = %s RETURNING *;""",
                (post.title, post.content, post.published, id))
    updated_post = cur.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    conn.commit()
    return {"data": updated_post}
