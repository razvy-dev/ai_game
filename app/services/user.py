from datetime import datetime, UTC, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from app.settings import settings

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

    @staticmethod
    async def sign_up():
        pass

    @staticmethod
    async def sign_in():
        pass

    @staticmethod
    async def forgot_password():
        pass

    @staticmethod
    async def reset_password():
        pass

    @staticmethod
    async def delete_account():
        pass