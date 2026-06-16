"""SEO Fundamentals scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("seo_fundamentals")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check fundamental SEO issues."""
    issues = []

    # Title tag
    title_tag = soup.find("title")
    if not title_tag or not title_tag.get_text(strip=True):
        issues.append({
            "title": "Missing <title> tag",
            "severity": "critical", "difficulty": "easy",
            "business_impact": "Search engines can't determine page topic. Major SEO impact.",
            "revenue_impact_pct": 20.0,
            "recommendation": "Add a descriptive, keyword-rich title tag (50-60 characters)",
            "fix_preview": "<title>Your Page Title | Business Name</title>",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })
    else:
        title_text = title_tag.get_text(strip=True)
        if len(title_text) > 60:
            issues.append({
                "title": "Title tag too long",
                "description": f"Title is {len(title_text)} chars (recommended: 50-60).",
                "severity": "medium", "difficulty": "easy",
                "business_impact": "Search engines may truncate long titles in SERPs",
                "revenue_impact_pct": 3.0,
                "recommendation": "Shorten title to 50-60 characters",
                "fix_price_cents": 2900, "is_quick_fix": True,
            })
        if len(title_text) < 30:
            issues.append({
                "title": "Title tag too short",
                "description": f"Title is only {len(title_text)} chars.",
                "severity": "low", "difficulty": "easy",
                "business_impact": "Missed opportunity for keyword inclusion",
                "recommendation": "Expand title to 50-60 characters with relevant keywords",
                "fix_price_cents": 2900, "is_quick_fix": True,
            })

    # Meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if not meta_desc or not meta_desc.get("content", "").strip():
        issues.append({
            "title": "Missing meta description",
            "severity": "high", "difficulty": "easy",
            "business_impact": "Search engines may auto-generate description, reducing CTR",
            "revenue_impact_pct": 8.0,
            "recommendation": "Add a compelling meta description (150-160 characters)",
            "fix_preview": '<meta name="description" content="Your compelling description here">',
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Heading hierarchy
    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0:
        issues.append({
            "title": "Missing H1 heading",
            "severity": "high", "difficulty": "easy",
            "business_impact": "H1 is a critical ranking signal and page structure element",
            "revenue_impact_pct": 5.0,
            "recommendation": "Add one H1 heading that describes the page content",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })
    elif len(h1_tags) > 1:
        issues.append({
            "title": f"Multiple H1 tags ({len(h1_tags)}) detected",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Dilutes semantic structure and ranking signals",
            "recommendation": "Use only one H1 per page; use H2-H6 for subsections",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Canonical tag
    canonical = soup.find("link", rel="canonical")
    if not canonical:
        issues.append({
            "title": "Missing canonical URL tag",
            "severity": "low", "difficulty": "easy",
            "business_impact": "May cause duplicate content issues",
            "recommendation": "Add rel='canonical' tag pointing to the preferred URL",
            "fix_preview": f'<link rel="canonical" href="{url}">',
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    return issues