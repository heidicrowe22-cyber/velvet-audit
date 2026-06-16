"""Mobile Responsiveness scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("mobile_responsiveness")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check mobile responsiveness issues."""
    issues = []

    # Check viewport meta tag
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if not viewport:
        issues.append({
            "title": "Missing viewport meta tag",
            "description": "No viewport meta tag found. Mobile devices will render the page at desktop width.",
            "severity": "critical",
            "difficulty": "easy",
            "business_impact": "Pages appear zoomed out on mobile, causing 30%+ bounce rate",
            "revenue_impact_pct": 15.0,
            "affected_element": "<head> section",
            "recommendation": "Add <meta name='viewport' content='width=device-width, initial-scale=1'> to the <head>",
            "fix_preview": '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "fix_price_cents": 2900,
            "is_quick_fix": True,
        })

    # Check if viewport has width=device-width
    if viewport:
        content = viewport.get("content", "")
        if "width=device-width" not in content:
            issues.append({
                "title": "Viewport meta tag not optimized",
                "description": "Viewport meta tag exists but doesn't set width=device-width properly.",
                "severity": "high",
                "difficulty": "easy",
                "business_impact": "Mobile users may have suboptimal viewing experience",
                "revenue_impact_pct": 8.0,
                "recommendation": "Update viewport content to 'width=device-width, initial-scale=1'",
                "fix_preview": '<meta name="viewport" content="width=device-width, initial-scale=1">',
                "fix_price_cents": 2900,
                "is_quick_fix": True,
            })

    # Check touch target sizes (look for small links)
    small_links = soup.find_all(["a", "button"])
    for link in small_links:
        onclick = link.get("onclick", "")
        href = link.get("href", "")
        text = link.get_text(strip=True)
        if text and len(text) < 3 and (href or onclick):
            issues.append({
                "title": "Small touch target detected",
                "description": f"Link/button '{text[:30]}' may be too small for mobile touch targets.",
                "severity": "medium",
                "difficulty": "medium",
                "business_impact": "Users may accidentally tap wrong elements on mobile",
                "revenue_impact_pct": 3.0,
                "recommendation": "Ensure touch targets are at least 44x44px with adequate spacing",
                "affected_element": f"<{link.name}>{text[:30]}</{link.name}>",
                "fix_price_cents": 7900,
                "is_quick_fix": False,
            })
            break  # Only flag one

    # Check for responsive CSS media queries
    has_media_queries = "@media" in html and ("max-width" in html or "min-width" in html)
    if not has_media_queries:
        issues.append({
            "title": "No responsive CSS media queries detected",
            "description": "The page doesn't appear to use CSS media queries for responsive design.",
            "severity": "high",
            "difficulty": "hard",
            "business_impact": "Site will not adapt to different screen sizes, losing mobile traffic",
            "revenue_impact_pct": 12.0,
            "recommendation": "Implement responsive design with CSS media queries or a mobile-first framework",
            "fix_price_cents": 29900,
            "is_quick_fix": False,
        })

    return issues