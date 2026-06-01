from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService

router = APIRouter(prefix='/api/v1/user', tags=['users'])

@router.post('/login')
async def log_in(db: AsyncSession = Depends(get_db)):
    pass


@router.post('/signup')
async def sign_up(db: AsyncSession = Depends(get_db)):
    pass


@router.post('/forgot-password')
async def forgot_password(db: AsyncSession = Depends(get_db)):
    pass


@router.post('/reset-password')
async def reset_password(db: AsyncSession = Depends(get_db)):
    pass


@router.post('/delete-account')
async def delete_account(db: AsyncSession = Depends(get_db)):
    pass