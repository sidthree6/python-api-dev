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
    published: bool = True


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.pid.desc()).first()
    return {"data": post}


@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@ app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pid == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"data": post}


@ app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.pid == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.pid == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": updated_post.first()}
