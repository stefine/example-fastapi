from app import schema, utils, models
from app.database import get_db
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_users(user: schema.UserRequest, db: Session = Depends(get_db)):
    hashed_paswd = utils.hash(user.password)
    user.password = hashed_paswd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schema.UserProfile)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message: post id with {id} doesn't exist")
    return user
