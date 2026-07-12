from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.issue import IssueCreate, IssueDelete, IssueEdit, IssueResponse
from app.models import Issue
from sqlalchemy.future import select
from fastapi import HTTPException

class IssueService:
    @staticmethod
    async def report_issue(db: AsyncSession, issue_data: IssueCreate) -> Issue:
        new_issue = Issue(
            title=issue_data.title,
            description=issue_data.description
        )

        db.add(new_issue)

        try:
            await db.commit()
            await db.refresh(new_issue)
            return new_issue

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Issue Creation Failed: {str(e)}")

    @staticmethod
    async def get_all_issues(db: AsyncSession) -> list[Issue]:
        result = await db.execute(select(Issue).order_by(Issue.reported_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def delete_issue(db: AsyncSession, issue_to_delete: IssueDelete) -> bool:
        pass

    async def edit_issue(db: AsyncSession, new_issue_data: IssueEdit) -> IssueResponse:
        pass
