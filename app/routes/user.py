from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService
from app.schemas.user import UserPrivateResponse, UserCreate, Token

router = APIRouter(prefix='/api/v1/user', tags=['users'])

@router.post(
    '/login',
    response_model=Token
)
async def log_in(db: AsyncSession = Depends(get_db)):
    return await UserService.sign_in()


@router.post(
    '/signup', 
    response_model=UserPrivateResponse,
    status_code=status.HTTP_201_CREATED
)
async def sign_up(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.sign_up(db=db, user_data=user_data)


@router.post('/forgot-password')
async def forgot_password(db: AsyncSession = Depends(get_db)):
    pass


@router.post('/reset-password')
async def reset_password(new_password: str, user_id: str, db: AsyncSession = Depends(get_db)):
    return await UserService.reset_password(db, new_password, user_id)


@router.post('/delete-account')
async def delete_account(user_id: str, db: AsyncSession = Depends(get_db)):
    return await UserService.delete_account(db, user_id)