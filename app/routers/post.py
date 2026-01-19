from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOutput])
def get_posts(db: Session = Depends(get_db), current_user=Depends(get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all())

    return posts


@router.get("/{id}", response_model=schemas.PostOutput)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(input_post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_post = models.Post(user_id=current_user.id, **(input_post.model_dump()))
    db.add(new_post)  # adds new_post to current sqlalchemy session
    db.commit()
    db.refresh(new_post)  # updates new_post from the database (to get full info)

    return new_post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform specific action.")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, input_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):  # receiving updated data from the frontend
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform specific action.")

    post_query.update(input_post.model_dump(),
                      synchronize_session=False)

    db.commit()

    updated_post = post_query.first()
    return updated_post
