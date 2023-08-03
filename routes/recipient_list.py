from fastapi import File, UploadFile, status, HTTPException, APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from models.models import RecipientList
from schema.schema import ResRecipient, NewRecipient
from datetime import datetime
from typing import List
from config.config import settings
from sqlalchemy.exc import SQLAlchemyError
from auth.auth import decode_jwt
import csv
# from utils.helpers import get_calories_from_api

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Utility function to get user from token
async def get_user_from_token(token: str):
    user_from_token = decode_jwt(token)
    if not user_from_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user_from_token


@router.post('/recipient/upload/', response_model=List[ResRecipient], status_code=status.HTTP_201_CREATED)
async def upload_recipient_csv(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    try:
        user_from_token = await get_user_from_token(token)
        user = user_from_token['user_id']

        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid file format. Only CSV files are allowed.")
        
        recipients = []

        # Baca file CSV dan tambahkan entri penerima ke daftar recipients
        contents = await file.read()
        decoded_content = contents.decode('utf-8')
        csv_reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
        for row in csv_reader:
            new_recipient = RecipientList(
                phone_number=row['phone_number'],
                fullname=row['fullname'],
                company=row['company'],
                status=row['status'],
                user_id=user,
                date=datetime.now().strftime("%Y-%m-%d"),
                time=datetime.now().strftime("%H:%M:%S"),
            )
            recipients.append(new_recipient)

        # Simpan semua entri penerima ke database
        db.add_all(recipients)
        db.commit()

        return recipients
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while saving data to the database.")





# Export the router
recipient_routes = router