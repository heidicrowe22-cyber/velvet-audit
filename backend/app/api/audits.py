"""Audit management API routes."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Website, Audit, AuditCategory, Issue, AuditStatus
from app.schemas.schemas import (
    AuditCreate, AuditResponse, AuditStatusResponse,
    AuditCategoryScore, IssueResponse,
)

router = APIRouter()


@router.post("/", response_model=AuditStatusResponse, status_code=status.HTTP_201_CREATED)
async def start_audit(
    data: AuditCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    """Start a new website audit."""
    from urllib.parse import urlparse
    url = data.website_url if data.website_url.startswith(("http://", "https://")) else f"https://{data.website_url}"
    domain = urlparse(url).netloc.lower()

    # Find or create website
    result = await db.execute(
        select(Website).where(Website.domain == domain, Website.user_id == user.id)
    )
    website = result.scalar_one_or_none()
    if not website:
        website = Website(
            user_id=user.id,
            url=url,
            domain=domain,
            name=domain,
        )
        db.add(website)
        await db.flush()

    # Create audit record
    audit = Audit(
        website_id=website.id,
        user_id=user.id,
        status=AuditStatus.PENDING,
    )
    db.add(audit)
    await db.flush()
    await db.refresh(audit)

    # Queue background scan (simplified - will be async task in production)
    if background_tasks:
        from app.scanner.scanner import run_audit_scan
        background_tasks.add_task(run_audit_scan, audit.id)

    return AuditStatusResponse.model_validate(audit)


@router.get("/", response_model=list[AuditStatusResponse])
async def list_audits(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all audits for the current user."""
    result = await db.execute(
        select(Audit)
        .where(Audit.user_id == user.id)
        .order_by(Audit.created_at.desc())
        .limit(50)
    )
    return [AuditStatusResponse.model_validate(a) for a in result.scalars().all()]


@router.get("/{audit_id}", response_model=AuditResponse)
async def get_audit(
    audit_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get full audit results including categories and issues."""
    result = await db.execute(
        select(Audit).where(Audit.id == audit_id, Audit.user_id == user.id)
    )
    audit = result.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    # Get categories
    cat_result = await db.execute(
        select(AuditCategory).where(AuditCategory.audit_id == audit_id)
    )
    categories = [AuditCategoryScore.model_validate(c) for c in cat_result.scalars().all()]

    # Get issues
    issue_result = await db.execute(
        select(Issue).where(Issue.audit_id == audit_id).order_by(Issue.severity)
    )
    issues = [IssueResponse.model_validate(i) for i in issue_result.scalars().all()]

    response = AuditResponse.model_validate(audit)
    response.categories = categories
    response.issues = issues
    return response


@router.get("/{audit_id}/status", response_model=AuditStatusResponse)
async def get_audit_status(
    audit_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current status of an audit."""
    result = await db.execute(
        select(Audit).where(Audit.id == audit_id, Audit.user_id == user.id)
    )
    audit = result.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return AuditStatusResponse.model_validate(audit)