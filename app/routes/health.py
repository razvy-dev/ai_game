from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix='/api/v1/health', tags=['health'])

@router.get('/')
def get_health():
    return {"status": "ok"}

@router.get("/database")
async def test_database_connection(db: AsyncSession = Depends(get_db)):
    """Verifies the backend can execute queries against Postgres."""
    try:
        # Run a simple raw SQL query to test connectivity
        result = await db.execute(text("SELECT 1"))
        return {"database": "healthy", "response": result.scalar()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")