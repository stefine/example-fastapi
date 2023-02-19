from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import schema, models, utils
from app.routers import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentation']
)


@router.post("/login", response_model=schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    email, password = user_credentials.username, user_credentials.password
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"message: the user {email} doesn't exist")
    if not utils.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"message: the password is not accurate")
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
