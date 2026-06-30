from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService
from app.schemas.user import UserPrivateResponse, UserPublicResponse, UserCreate, UserLogin, Token, UserEdit
from datetime import timedelta

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

@router.post(
    '/sign-in',
    response_model=Token
)
async def log_in(sign_in_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await UserService.sign_in(db, sign_in_data)


@router.post(
    '/sign-up', 
    response_model=UserPrivateResponse,
    status_code=status.HTTP_201_CREATED
)
async def sign_up(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.sign_up(db=db, user_data=user_data)

@router.get(
    '/{user_id}',
    response_model=UserPublicResponse
)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)) -> UserPublicResponse:
    return await UserService.get_user(db, user_id)

@router.put(
    '/edit/{user_id}',
    response_model=UserPrivateResponse
)
async def edit_user(new_user_data: UserEdit, db: AsyncSession = Depends(get_db)):
    return await UserService.edit_user(db=db, new_user_data=new_user_data)


@router.post('/forgot-password')
async def forgot_password(db: AsyncSession = Depends(get_db)):
    pass


@router.post('/reset-password')
async def reset_password(new_password: str, user_id: str, db: AsyncSession = Depends(get_db)):
    return await UserService.reset_password(db, new_password, user_id)


@router.post('/delete-account')
async def delete_account(user_id: str, db: AsyncSession = Depends(get_db)):
    return await UserService.delete_account(db, user_id)