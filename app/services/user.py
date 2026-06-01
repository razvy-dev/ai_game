from datetime import datetime, UTC, timedelta
import jwt
import uuid
from fastapi.security import OAuth2PasswordBearer, HTTPException, status
from pwdlib import PasswordHash
from app.settings import settings
from app.schemas.user import UserCreate, UserPublicResponse, UserPrivateResponse, Token
from app.models.user import User


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")

class UserService:
    __password_hash = PasswordHash.recommended()

    __oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")

    def __hash_password(password: str) -> str:
        return __pasword_hash.hash(password)

    def __verify_password(plain_password: str, hashed_password: str):
        return __pasword_hash.verify(plain_password == hashed_password)

    def __create_access_token(data: dict, expires_delta: timedelta | None = None):
        """ Create an access JWT token """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else: 
            expire = datetime.now(UTC) + timedelta(
                minutes = settings.access_token_expires_in_minutes
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, 
            settings.secret_key.get_secret_value(),
            settings.algorithm
        )

        return encoded_jwt

    def __verify_access_token(token: str) -> str | None:
        """ Verify the access token """

        try:
            payload = jwt.decode(
                token,
                settings.secret_key.get_secret_value(),
                algorithm = [settings.algorithm],
                options = {"require": ["exp", "sub"]}
            )

        except jwt.InvalidTokenError:
            return None

        except Exception as e:
            print("Something went terribly wrong here")

        else:
            return payload.get("sub")

    def __check_if_user_exists_by_email(db: AsyncSession, email: str) -> bool:
        result = await db.execute(
            select(models.User).where(models.User.email == email)
        )

        existing = result.scalars().first()

        if existing:
            return True
        else:
            return False

    def __cehck_if_user_exists_by_username(db: AsyncSession, username: str) -> bool:
        result = await db.execute(
            select(models.User).where(models.User.username == username)
        )

        existing = result.scalars().first()

        if existing:
            return True
        else:
            return False

    @staticmethod
    async def sign_up(self, db: AsyncSession, user_data: UserCreate) -> UserPrivateResponse:
        # check if the user already exists

        by_email = self.__check_if_user_exists_by_email(db, user_data.email)
        by_username = self.__check_if_user_exists_by_username(db, user_data.username)

        if by_email or by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        # if i got here, it means the user does not exist, so I can create it

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=self.__hash_password(user_data.password),
            phone=user_data.phone,
            image=user_data.image,
            ip=user_data.ip
        )

        try:
            await db.commit()
            await db.refresh(new_user)
            return new_user

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Yeah, sign up basically failed: {str(e)}")
        
        # TODO: implement account verification using resend

    @staticmethod
    async def sign_in(self, db: AsyncSession, sign_in_data) -> UserPrivateResponse:
        # first of all, look him up in the database

        result = await db.execute(select(User).where(User.email == sign_in_data.email))

        user = result.scalars().first()

        if not user or not self.__verify_password(sign_in_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Either the password is wrong or the account does not exist"
            )

        # if I got here, it means the account and the passworrd were correct, so I give back the access token

        access_token_expires = timedelta(minuts=settings.access_token_expires_in_minutes)
        access_token = self.__create_access_token(
            data={
                "sub": str(user.id)
            },
            expires_delta=access_token_expires
        )

        return Token(access_token=acess_token, token_type='Bearer')

    @staticmethod
    async def forgot_password():
        pass # TODO: I can't implement this until I integrate resend in here

    @staticmethod
    async def reset_password(db: AsyncSession, new_password: str, user_id: uuid.uuid4) -> UserPrivateResponse:
        hashed_password = self.__hash_password(new_password)
        try:
            result = await db.execute(update(User.password).where(User.id == user_id).set(new_password))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Setting a new passowrd for this account didn't work: {str(e)}")

    @staticmethod
    async def delete_account(db: AsyncSession, user_id: uuid.uuid4) -> bool: # a bool here to measure success
        try:
            result = await db.execute(delete(User).where(User.id == user_id))

            if result:
                return True
            else:
                return False
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Deleting this account didn't work: {str(e)}")