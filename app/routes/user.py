from fastapi import APIRouter, Depends, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService
from app.schemas.user import UserPrivateResponse, UserPublicResponse, UserCreate, UserLogin, Token, UserEdit, UserResetPassword, UserForgotPassword
from app.deps import get_current_user_id

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

@router.post(
    '/sign-in',
    response_model=UserPrivateResponse
)
async def log_in(sign_in_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await UserService.sign_in(db, sign_in_data)


@router.post(
    '/sign-up', 
    status_code=status.HTTP_201_CREATED
)
async def sign_up(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.sign_up(db=db, user_data=user_data)

@router.get('/confirm-account', response_model=UserPrivateResponse, status_code=status.HTTP_200_OK)
async def confirm_account(token: str, db: AsyncSession = Depends(get_db)):
    return await UserService.confirm_account(db=db, validation_token=token)

@router.post('/forgot-password')
async def forgot_password(data: UserForgotPassword, db: AsyncSession = Depends(get_db)):
    return await UserService.forgot_password(db, data)


@router.post(
    '/reset-password',
    status_code=status.HTTP_200_OK
)
async def reset_password(data: UserResetPassword, db: AsyncSession = Depends(get_db)):
    if (data.currentPassword):
        user_id = get_current_user_id()

    return await UserService.reset_password(db, data)

@router.post('/delete-account')
async def delete_account(user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    return await UserService.delete_account(db, user_id)

@router.get(
    '/edit/{user_id}',
    response_model=UserPrivateResponse
)
async def edit_user(new_user_data: UserEdit, user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    return await UserService.edit_user(db=db, user_id=user_id, new_user_data=new_user_data)

@router.get(
    '/me',
    response_model=UserPrivateResponse
)
async def get_my_data(user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    return await UserService.get_my_data(user_id, db)

@router.get(
    '/{ussrname}',
    response_model=UserPublicResponse
)
async def get_user(username: str, db: AsyncSession = Depends(get_db)) -> UserPublicResponse:
    return await UserService.get_user(db, username)