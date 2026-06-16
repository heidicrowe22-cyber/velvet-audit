"""Fix/pricing API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, FixPackage, Issue, Audit
from app.schemas.schemas import (
    FixPackageResponse,
    FixEstimateRequest,
    FixEstimateResponse,
)

router = APIRouter()


@router.get("/packages", response_model=list[FixPackageResponse])
async def list_fix_packages(db: AsyncSession = Depends(get_db)):
    """List all available fix packages."""
    result = await db.execute(select(FixPackage))
    packages = result.scalars().all()

    if not packages:
        # Seed default packages on first access
        default_packages = [
            FixPackage(id="quick_fix", name="Quick Fix", price_cents=2900,
                       estimated_days=1, is_bundle=False,
                       description="Simple text/code change for a single issue"),
            FixPackage(id="standard_fix", name="Standard Fix", price_cents=7900,
                       estimated_days=2, is_bundle=False,
                       description="Moderate complexity fix for one category"),
            FixPackage(id="category_fix", name="Category Fix", price_cents=14900,
                       estimated_days=3, is_bundle=False,
                       description="Full optimization of one audit category"),
            FixPackage(id="bundle_fix", name="Bundle Fix", price_cents=29900,
                       estimated_days=5, is_bundle=True,
                       description="3-5 related fixes across categories"),
        ]
        for pkg in default_packages:
            db.add(pkg)
        await db.flush()
        for pkg in default_packages:
            await db.refresh(pkg)
        packages = default_packages

    return [FixPackageResponse.model_validate(p) for p in packages]


@router.post("/estimate", response_model=FixEstimateResponse)
async def estimate_fix_cost(
    data: FixEstimateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Estimate cost for fixing specific issues."""
    total_cents = 0
    packages = []
    max_days = 0

    for issue_id in data.issue_ids:
        result = await db.execute(
            select(Issue).where(Issue.id == issue_id, Issue.audit_id == data.audit_id)
        )
        issue = result.scalar_one_or_none()
        if issue and issue.fix_price_cents:
            total_cents += issue.fix_price_cents

    # Determine best package(s)
    pkg_result = await db.execute(select(FixPackage))
    all_pkgs = pkg_result.scalars().all()

    if not all_pkgs:
        # Fallback pricing
        if total_cents <= 2900:
            packages.append(FixPackageResponse(
                id="quick_fix", name="Quick Fix", price_cents=2900,
                estimated_days=1, is_bundle=False,
                description="Simple text/code change for a single issue"
            ))
            max_days = 1
        elif total_cents <= 7900:
            packages.append(FixPackageResponse(
                id="standard_fix", name="Standard Fix", price_cents=7900,
                estimated_days=2, is_bundle=False,
                description="Moderate complexity fix"
            ))
            max_days = 2
        else:
            packages.append(FixPackageResponse(
                id="bundle_fix", name="Bundle Fix", price_cents=29900,
                estimated_days=5, is_bundle=True,
                description="3-5 related fixes across categories"
            ))
            max_days = 5
        total_cents = packages[0].price_cents
    else:
        for pkg in all_pkgs:
            packages.append(FixPackageResponse.model_validate(pkg))
            max_days = max(max_days, pkg.estimated_days or 1)
        total_cents = max(total_cents, min(p.price_cents for p in all_pkgs))

    return FixEstimateResponse(
        total_cents=total_cents,
        packages=packages,
        estimated_days=max_days,
    )