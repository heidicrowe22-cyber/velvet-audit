"""Report generation API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Audit, ReportSnapshot, AuditCategory, Issue
from app.schemas.schemas import ReportResponse

router = APIRouter()


@router.get("/{audit_id}", response_model=ReportResponse)
async def get_report(
    audit_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the report for a completed audit."""
    # Check audit exists and belongs to user
    audit_result = await db.execute(
        select(Audit).where(Audit.id == audit_id, Audit.user_id == user.id)
    )
    audit = audit_result.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")

    # Try to get existing snapshot
    snap_result = await db.execute(
        select(ReportSnapshot)
        .where(ReportSnapshot.audit_id == audit_id)
        .order_by(ReportSnapshot.generated_at.desc())
        .limit(1)
    )
    snapshot = snap_result.scalar_one_or_none()

    if snapshot:
        return ReportResponse.model_validate(snapshot)

    # Generate on the fly from audit data
    cat_result = await db.execute(
        select(AuditCategory).where(AuditCategory.audit_id == audit_id)
    )
    categories = cat_result.scalars().all()

    issue_result = await db.execute(
        select(Issue).where(Issue.audit_id == audit_id).order_by(Issue.severity)
    )
    issues = issue_result.scalars().all()

    category_scores = {c.category_name: c.score for c in categories}
    issue_summary = {
        "total": len(issues),
        "critical": sum(1 for i in issues if i.severity.value == "critical"),
        "high": sum(1 for i in issues if i.severity.value == "high"),
        "medium": sum(1 for i in issues if i.severity.value == "medium"),
        "low": sum(1 for i in issues if i.severity.value == "low"),
        "info": sum(1 for i in issues if i.severity.value == "info"),
    }

    top_issues = [
        {"title": i.title, "severity": i.severity.value, "category": i.category_name}
        for i in issues[:5]
    ]

    quick_wins = [
        {"title": i.title, "fix_price_cents": i.fix_price_cents}
        for i in issues if i.is_quick_fix
    ][:3]

    # Create snapshot
    snapshot = ReportSnapshot(
        audit_id=audit_id,
        overall_score=audit.overall_score or 0,
        category_scores=category_scores,
        issue_summary=issue_summary,
        top_issues=top_issues,
        quick_wins=quick_wins,
        summary_text=f"Audit completed with overall score of {audit.overall_score:.0f}/100. "
                     f"Found {issue_summary['total']} issues ({issue_summary['critical']} critical, "
                     f"{issue_summary['high']} high, {issue_summary['medium']} medium).",
        is_published=True,
    )
    db.add(snapshot)
    await db.flush()
    await db.refresh(snapshot)

    return ReportResponse.model_validate(snapshot)