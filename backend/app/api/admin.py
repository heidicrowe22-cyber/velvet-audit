"""Admin API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import require_admin
from app.models.models import (
    User, Audit, Order, Implementation, ImplementationStatus,
    UserRole,
)
from app.schemas.schemas import (
    UserResponse, AuditStatusResponse, OrderResponse, ImplementationResponse,
)

router = APIRouter()


@router.get("/customers", response_model=list[UserResponse])
async def list_customers(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all customer accounts."""
    result = await db.execute(
        select(User).where(User.role == UserRole.CUSTOMER).order_by(User.created_at.desc())
    )
    return [UserResponse.model_validate(u) for u in result.scalars().all()]


@router.get("/audits", response_model=list[AuditStatusResponse])
async def list_all_audits(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all audits across all customers."""
    result = await db.execute(
        select(Audit).order_by(Audit.created_at.desc()).limit(100)
    )
    return [AuditStatusResponse.model_validate(a) for a in result.scalars().all()]


@router.get("/implementations", response_model=list[ImplementationResponse])
async def list_implementations(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List implementation queue."""
    result = await db.execute(
        select(Implementation).order_by(Implementation.created_at.asc())
    )
    return [ImplementationResponse.model_validate(i) for i in result.scalars().all()]


@router.get("/stats")
async def get_stats(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get platform statistics."""
    user_count = await db.scalar(select(func.count(User.id)))
    audit_count = await db.scalar(select(func.count(Audit.id)))
    order_count = await db.scalar(select(func.count(Order.id)))
    impl_pending = await db.scalar(
        select(func.count(Implementation.id))
        .where(Implementation.status == ImplementationStatus.QUEUED)
    )
    avg_score = await db.scalar(select(func.avg(Audit.overall_score)))

    return {
        "total_customers": user_count or 0,
        "total_audits": audit_count or 0,
        "total_orders": order_count or 0,
        "pending_implementations": impl_pending or 0,
        "average_audit_score": round(avg_score or 0, 1),
    }


@router.patch("/implementations/{impl_id}/status")
async def update_implementation_status(
    impl_id: str,
    data: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update implementation status."""
    result = await db.execute(
        select(Implementation).where(Implementation.id == impl_id)
    )
    impl = result.scalar_one_or_none()
    if not impl:
        raise HTTPException(status_code=404, detail="Implementation not found")

    new_status = data.get("status")
    if new_status:
        try:
            impl.status = ImplementationStatus(new_status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {new_status}")

    if data.get("notes"):
        impl.notes = data["notes"]

    await db.flush()
    await db.refresh(impl)
    return ImplementationResponse.model_validate(impl)