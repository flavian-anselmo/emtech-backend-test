from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schema import schema
from app.utils import auth_utils
from app.oauth import oauth2


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def sign_up(user: schema.UserCreate,db: Session = Depends(get_db)):
    """
    Create user account
    """

    existing_user = db.query(models.Users).filter(models.Users.username == user.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    hashed_password = auth_utils.get_hashed_password(user.password)
    user.password = hashed_password
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post("/sign-in", status_code=status.HTTP_200_OK, response_model=schema.TokenResponse)
def sign_in(user_creds: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    """
    Login user
    """

    # check user exists
    user = db.query(models.Users).filter(models.Users.username == user_creds.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # verify password
    if not auth_utils.verify_password(user_creds.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password"
        )
    # create token
    access_token = oauth2.create_access_token(
        payload={
            "user_id": user.user_id,
            "role": user.role
        }
    )
    return schema.TokenResponse(
        access_token=access_token,
        token_type="Bearer"
    )