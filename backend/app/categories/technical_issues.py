"""Technical Issues scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("technical_issues")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check technical issues."""
    issues = []

    # Check for broken internal links (simple check - find incomplete links)
    all_links = soup.find_all("a", href=True)
    broken_refs = []
    for a in all_links:
        href = a.get("href", "")
        if href in ("#", "javascript:void(0)", "javascript:void(0);", "", " ", "#!"):
            broken_refs.append(href)

    if broken_refs:
        issues.append({
            "title": f"{len(broken_refs)} link(s) with empty/placeholder href",
            "description": "Links with '#' or 'javascript:void(0)' provide no navigation.",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Broken UX for users and search engine crawlers",
            "recommendation": "Replace placeholder links with actual URLs or remove them",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    # Check for missing favicon
    favicon_links = soup.find_all("link", rel=re.compile(r"icon|shortcut icon", re.I))
    if not favicon_links:
        issues.append({
            "title": "No favicon detected",
            "severity": "low", "difficulty": "easy",
            "business_impact": "Browser tabs show generic icon. Minor branding miss.",
            "recommendation": "Add a favicon to your website",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Check for 404 errors (heuristic: check page title)
    title = soup.find("title")
    if title and re.search(r'404|not found|page not found', title.get_text(), re.I):
        issues.append({
            "title": "Page returns 404 Not Found",
            "severity": "critical", "difficulty": "easy",
            "business_impact": "Users landing here will leave immediately",
            "revenue_impact_pct": 30.0,
            "recommendation": "Redirect this page or restore the content",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Check for missing sitemap reference
    has_sitemap = bool(soup.find("link", rel="sitemap")) or "/sitemap.xml" in html.lower()
    if not has_sitemap:
        issues.append({
            "title": "No sitemap reference found",
            "severity": "low", "difficulty": "medium",
            "business_impact": "Search engines may miss pages during crawling",
            "recommendation": "Create and submit an XML sitemap to search engines",
            "fix_price_cents": 7900, "is_quick_fix": False,
        })

    # Check for console errors (cannot actually detect JS errors server-side, but can flag)
    issues.append({
        "title": "JavaScript errors not checked (server-side scan limitation)",
        "severity": "info", "difficulty": "medium",
        "business_impact": "JS errors can break page functionality silently",
        "recommendation": "Use browser DevTools Console to check for JavaScript errors",
        "fix_price_cents": 2900, "is_quick_fix": True,
    })

    return issues


import re