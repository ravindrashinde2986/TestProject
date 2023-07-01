from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import Vote
from sqlalchemy.orm import Session
from .. database import get_db
from sqlalchemy.exc import IntegrityError
from ..oauth2 import get_current_user
from ..models import Vote as VoteModel

router = APIRouter(tags=['Votes'])


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session= Depends(get_db), user: dict = Depends(get_current_user)):
    vote_record_q = db.query(VoteModel).filter(VoteModel.post_id == vote.post_id, VoteModel.user_id == user.id)
    if not vote.like:
        vote_record = vote_record_q.first()
        if vote_record:
            vote_record_q.delete()
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote for post id {vote.post_id} does not exist")
    else:
        try:
            vt = VoteModel(post_id=vote.post_id, user_id=user.id)
            db.add(vt)
            db.commit()
            db.refresh(vt)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"vote for post id {vote.post_id} already exist")

        return vt




