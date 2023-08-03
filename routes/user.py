from fastapi import status, HTTPException, APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import User
from schema.schema import NewUser, ResUser, Login, Role, DeletionSuccess, ResUpdateUser
from datetime import datetime
from auth.auth import sign_jwt
from sqlalchemy.exc import SQLAlchemyError
from typing import List
# from .entry import get_user_from_token
from utils.helpers import hash_password, verify_hashed_password

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



# Endpoint for creating a new user
@router.post('/signup/', response_model=ResUser, status_code=status.HTTP_201_CREATED)
async def create_a_user(user: NewUser):
    # Hash the user's password
    hashed_password = await hash_password(user.password)

    # Create a new user object
    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password=hashed_password,
        role=user.role,
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M:%S"),
    )

    # Check if a user with the same email already exists
    db_item = db.query(User).filter(User.email == new_user.email).first()

    if db_item is not None:
        raise HTTPException(status_code=400, detail="User with the email already exists")

    # Add the new user to the database
    db.add(new_user)
    db.commit()

    return new_user




# Endpoint for user login
@router.post('/login/')
async def login_a_user(login: Login):
    try:
        db_user = db.query(User).filter(User.email == login.email).first()

        if db_user is not None:
            # Verify the user's password
            is_password_valid = await verify_hashed_password(login.password, db_user.password)

            if not is_password_valid:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have entered a wrong password")
            
            if is_password_valid:
                # Generate a JWT access token for authentication
                token = sign_jwt(db_user)
                return token
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have entered a wrong password")
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the database")



# Endpoint for retrieving a list of users
@router.get('/users/', response_model=List[ResUser], status_code=200)
async def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    token: str = Depends(oauth2_scheme)
):
    try:
        user_from_token = await get_user_from_token(token)
        role = Role(user_from_token['role'])
        user_email = user_from_token['user_email']
        offset = (page - 1) * per_page

        if role == Role.ADMIN:
            user_entries = db.query(User).offset(offset).limit(per_page).all()
        elif role == Role.MANAGER:
            user_entries = db.query(User).filter(User.role == Role.USER).offset(offset).limit(per_page).all()
        elif role == Role.USER:
            user_entries = db.query(User).filter(User.email == user_email).first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")

        # return user_entries
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Export the router
user_routes = router