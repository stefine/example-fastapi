from app import schema, utils, models
from app.database import get_db
from fastapi import status, Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session

from app.routers.oauth2 import get_current_user

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schema.Vote, db: Session = Depends(get_db),
               current_user=Depends(get_current_user)):
    post_id, user_id = vote.post_id, current_user.id
    sql = db.query(models.Votes).filter(models.Votes.post_id == post_id,
                                        models.Votes.user_id == user_id)
    record = sql.first()
    if vote.dir == 1:
        if not record:
            liking = models.Votes(user_id=user_id, post_id=post_id)
            db.add(liking)
            db.commit()
            return {"message": "successfully added vote"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {user_id} already on the post {post_id}")
    else:
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with {post_id} doesn't exist")
        sql.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
