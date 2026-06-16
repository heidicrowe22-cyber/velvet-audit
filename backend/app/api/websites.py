"""Website management API routes."""

from urllib.parse import urlparse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Website
from app.schemas.schemas import WebsiteCreate, WebsiteResponse

router = APIRouter()


def extract_domain(url: str) -> str:
    """Extract clean domain from a URL."""
    parsed = urlparse(url if url.startswith(("http://", "https://")) else f"https://{url}")
    return parsed.netloc.lower()


def detect_platform(domain: str, html: str = "") -> str:
    """Detect website platform by domain hints or HTML markers."""
    platform_map = {
        "wordpress": ["wordpress", "wp-"],
        "shopify": ["shopify", "myshopify"],
        "wix": ["wix", "wixstatic"],
        "squarespace": ["squarespace"],
        "webflow": ["webflow"],
        "godaddy": ["godaddy", "secureserver"],
    }
    domain_lower = domain.lower()
    html_lower = html.lower()
    for platform, keywords in platform_map.items():
        for kw in keywords:
            if kw in domain_lower or kw in html_lower:
                return platform
    return "custom"


@router.post("/", response_model=WebsiteResponse, status_code=status.HTTP_201_CREATED)
async def create_website(
    data: WebsiteCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Register a new website for auditing."""
    domain = extract_domain(data.url)
    platform = data.platform or detect_platform(domain)

    website = Website(
        user_id=user.id,
        url=data.url if data.url.startswith(("http://", "https://")) else f"https://{data.url}",
        domain=domain,
        platform=platform,
        name=data.name or domain,
    )
    db.add(website)
    await db.flush()
    await db.refresh(website)
    return WebsiteResponse.model_validate(website)


@router.get("/", response_model=list[WebsiteResponse])
async def list_websites(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all websites for the current user."""
    result = await db.execute(
        select(Website).where(Website.user_id == user.id).order_by(Website.created_at.desc())
    )
    return [WebsiteResponse.model_validate(w) for w in result.scalars().all()]


@router.get("/{website_id}", response_model=WebsiteResponse)
async def get_website(
    website_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get details for a specific website."""
    result = await db.execute(
        select(Website).where(Website.id == website_id, Website.user_id == user.id)
    )
    website = result.scalar_one_or_none()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    return WebsiteResponse.model_validate(website)