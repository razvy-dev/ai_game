from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.schemas.issue import IssueResponse, IssueCreate, IssueDelete, IssueEdit
from app.services.issue import IssueService

router = APIRouter(prefix='/api/v1/issue', tags=['issue'])

@router.get('/', response_model=list[IssueResponse])
async def get_issues(db: AsyncSession = Depends(get_db)):
    return await IssueService.get_all_issues(db=db)

@router.post('/add_issue', response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def add_issue(issue_in: IssueCreate, db: AsyncSession = Depends(get_db)):
    return await IssueService.report_issue(db=db, issue_data=issue_in)

@router.put('/edit_issue')
async def edit_issue():
    pass

@router.delete('/delete_issue')
async def delete_issue():
    pass