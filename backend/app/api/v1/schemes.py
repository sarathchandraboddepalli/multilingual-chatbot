from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.scheme import SchemeCreate, SchemeOut
from app.services.scheme_service import create_scheme, list_schemes, get_scheme

router = APIRouter()


@router.get("/", response_model=list[SchemeOut])
async def list_all_schemes(db: AsyncSession = Depends(get_db)):
    return await list_schemes(db)


@router.post("/", response_model=SchemeOut)
async def add_scheme(data: SchemeCreate, db: AsyncSession = Depends(get_db)):
    return await create_scheme(db, data)


@router.get("/{scheme_id}", response_model=SchemeOut)
async def get_scheme_detail(scheme_id: str, db: AsyncSession = Depends(get_db)):
    scheme = await get_scheme(db, scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme
