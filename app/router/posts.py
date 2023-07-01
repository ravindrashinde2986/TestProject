from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Post as PostModel, Vote as VoteModel
from ..schemas import Post, CreatePost, UpdatePost, PostVote
from ..oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostVote])
def get_posts(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    # cur.execute(""" select * from post""")
    # posts = cur.fetchall()
    # posts = db.query(PostModel).all()
    q = db.query(PostModel, func.count(VoteModel.post_id).label("votes")).join(VoteModel,
                                                                               PostModel.id == VoteModel.post_id,
                                                                               isouter=True).group_by(PostModel.id)

    posts = q.all()

    return posts


@router.get("/latest", response_model=Post)
def get_latest_post(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    # p = find_post(current_post_id)
    p = db.query(PostModel).order_by(desc(PostModel.id)).first()

    return p


@router.get("/{id}", response_model=PostVote)
def get_post(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):

    # p = db.query(PostModel).filter(PostModel.id == id).first()
    q = db.query(PostModel, func.count(VoteModel.post_id).label("votes"))\
        .join(VoteModel, PostModel.id == VoteModel.post_id, isouter=True).filter(PostModel.id == id).group_by(PostModel.id)

    p = q.first()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post found with id {id}")
    return p


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: CreatePost, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):

    new_post = PostModel(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    delete_post_q = db.query(PostModel).filter(PostModel.id == id)
    post_to_delete = delete_post_q.first()
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no post found with id {id}")

    if not post_to_delete.owner_id == user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not Authorized to delete the post !")

    delete_post_q.delete()
    db.commit()


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id: int, post: UpdatePost, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    update_post_q = db.query(PostModel).filter(PostModel.id == id)
    post_to_update = update_post_q.first()
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exists")
    if post_to_update.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not Authorized to update the post !")

    update_post_q.update(post.dict())
    db.commit()

    return update_post_q.first()
