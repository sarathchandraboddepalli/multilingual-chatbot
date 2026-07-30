from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate
from app.services.rag_service import index_scheme


async def create_scheme(db: AsyncSession, data: SchemeCreate) -> Scheme:
    scheme = Scheme(**data.model_dump())
    db.add(scheme)
    await db.commit()
    await db.refresh(scheme)
    index_scheme(
        scheme.scheme_id,
        scheme.name,
        scheme.description,
        scheme.eligibility or "",
        scheme.benefits or "",
        scheme.documents_required or "",
        scheme.application_url or "",
    )
    return scheme


async def list_schemes(db: AsyncSession) -> list[Scheme]:
    result = await db.execute(select(Scheme).where(Scheme.is_active == True).order_by(Scheme.name))
    return list(result.scalars().all())


async def get_scheme(db: AsyncSession, scheme_id: str) -> Scheme | None:
    result = await db.execute(select(Scheme).where(Scheme.scheme_id == scheme_id))
    return result.scalar_one_or_none()
