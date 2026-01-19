from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import InputVote
from ..database import get_db
from ..models import Vote, User, Post
from ..oauth2 import get_current_user

router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: InputVote, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post.id} does not exist.")

    vote_query = db.query(Vote).filter(Vote.user_id == current_user.id, Vote.post_id == vote.post_id)

    vote_found = vote_query.first()

    if vote.placing_vote:
        # placing a vote
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')

        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    else:
        # removing a vote
        # we cannot remove a vote that does not exist
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
