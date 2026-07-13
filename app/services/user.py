from datetime import datetime, UTC, timedelta
import token
import jwt
import uuid
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from app.settings import settings
from sqlalchemy import select, update, delete, func
from app.schemas.user import UserCreate, UserLogin, UserPublicResponse, UserPrivateResponse, Token, UserEdit
from app.models.user import User
from app.services.email import EmailService

class UserService:
    __password_hash = PasswordHash.recommended()

    __oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/token")

    @staticmethod
    def __hash_password(password: str) -> str:
        return UserService.__password_hash.hash(password)

    @staticmethod
    def __verify_password(plain_password: str, hashed_password: str) -> bool:
        return UserService.__password_hash.verify(plain_password, hashed_password)

    @staticmethod
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

    @staticmethod
    def __verify_access_token(token: str) -> str | None:
        """ Verify the access token """

        try:
            payload = jwt.decode(
                token,
                settings.secret_key.get_secret_value(),
                algorithms = [settings.algorithm],
                options = {"require": ["exp", "sub"]}
            )

        except jwt.InvalidTokenError as e:
            print(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The validation token is invalid or has expired: {str(e)}"
            )

        except Exception as e:
            print("Something went terribly wrong here")

        else:
            return payload.get("sub")

    @staticmethod
    async def __check_if_user_exists_by_email(db: AsyncSession, email: str) -> bool:
        result = await db.execute(
            select(User).where(User.email == email)
        )

        existing = result.scalars().first()

        if existing:
            return True
        else:
            return False

    @staticmethod
    async def __check_if_user_exists_by_username(db: AsyncSession, username: str) -> bool:
        result = await db.execute(
            select(User).where(User.username == username)
        )

        existing = result.scalars().first()

        if existing:
            return True
        else:
            return False

    @staticmethod
    async def sign_up(db: AsyncSession, user_data: UserCreate) -> None:
        by_email = await UserService.__check_if_user_exists_by_email(db, user_data.email)
        by_username = await UserService.__check_if_user_exists_by_username(db, user_data.username)

        if by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists"
            )

        if by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this username already exists"
            )

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=UserService.__hash_password(user_data.password),
            image=user_data.image,
            ip=user_data.ip
        )

        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Sign up failed: {str(e)}")

        try:
            validation_code_expires = timedelta(minutes=settings.access_token_expires_in_minutes)
            validation_token = UserService.__create_access_token(
                data={"sub": str(new_user.id), "purpose": "confirm_account"},
                expires_delta=validation_code_expires
            )
            EmailService.send_confirmation_email(to=user_data.email, validation_code=validation_token)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Sending the confirmation email failed: {str(e)}")
    

    async def confirm_account(db: AsyncSession, validation_token: str) -> UserPrivateResponse:
        user_id = UserService.__verify_access_token(validation_token)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The validation token is invalid or has expired"
            )

        user_uuid = uuid.UUID(user_id)

        try:
            result = await db.execute(
                update(User).where(User.id == user_uuid).values(confirmed_at=func.now())
            )

            if result.rowcount <= 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            await db.commit()

            user_result = await db.execute(select(User).where(User.id == user_uuid))
            user = user_result.scalars().first()

            access_token_expires = timedelta(minutes=settings.access_token_expires_in_minutes)
            access_token = UserService.__create_access_token(
                data={"sub": user_id},
                expires_delta=access_token_expires
            )

            return UserPrivateResponse(
                id=str(user.id),
                username=user.username,
                email=user.email,
                image=user.image,
                description=user.description,
                token=Token(access_token=access_token, token_type='Bearer')
            )

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Confirming the account failed: {str(e)}")


    @staticmethod
    async def sign_in(db: AsyncSession, sign_in_data: UserLogin) -> Token:
        result = await db.execute(select(User).where(User.email == sign_in_data.email))

        user = result.scalars().first()

        if not user or not UserService.__verify_password(sign_in_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Either the password is wrong or the account does not exist"
            )

        access_token_expires = timedelta(minutes=settings.access_token_expires_in_minutes)
        access_token = UserService.__create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type='Bearer')

    @staticmethod
    async def forgot_password():
        pass # TODO: I can't implement this until I integrate resend in here

    @staticmethod
    async def reset_password(db: AsyncSession, new_password: str, token: str) -> UserPrivateResponse:
        # check if he is allowed to reset the password
        try:
            payload = jwt.decode(
                token,
                settings.secret_key.get_secret_value(),
                algorithms=[settings.algorithm],
                options={"require": ["exp", "sub", "purpose"]}
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The reset token is invalid or has expired: {str(e)}"
            )

        if payload.get("purpose") != "reset_password":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This token is not valid for password resets"
            )

        user_id = uuid.UUID(payload.get("sub"))

        hashed_password = UserService.__hash_password(new_password)
        try:
            result = await db.execute(
                update(User).where(User.id == user_id).values(password=hashed_password)
            )
            await db.commit()

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Setting a new password for this account didn't work: {str(e)}")

    @staticmethod
    async def delete_account(db: AsyncSession, user_id: uuid.UUID) -> bool:
        try:
            result = await db.execute(delete(User).where(User.id == user_id))
            await db.commit()

            if result.rowcount > 0:
                return True
            else:
                return False
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Deleting this account didn't work: {str(e)}")

    @staticmethod
    async def edit_user(db: AsyncSession, new_user_data: UserEdit) -> UserPrivateResponse:
        try:
            result = await db.execute(
                update(User).where(User.id == new_user_data.id).values(**new_user_data.model_dump(exclude_unset=True))
            )
            await db.commit()

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"This operation failed because of: {str(e)}")

    @staticmethod
    async def get_user(db: AsyncSession, user_id: str) -> UserPublicResponse:
        try:
            result = await db.execute(select(User).where(User.id == user_id))

            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=404, detail=f"there is not user with this id")

            return UserPublicResponse(
                username=user.username,
                description=user.description,
                image=user.image
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"This operation kinda failed")