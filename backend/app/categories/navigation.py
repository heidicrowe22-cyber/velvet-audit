"""Navigation scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("navigation")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check navigation issues."""
    issues = []

    # Check for navigation menu
    nav_tags = soup.find_all("nav")
    has_nav = len(nav_tags) > 0

    # Also check for common nav class/id patterns
    nav_selectors = ["menu", "navigation", "navbar", "nav-menu", "main-menu", "top-menu"]
    has_nav_by_class = any(soup.find(class_=re.compile(c, re.I)) for c in nav_selectors)
    has_nav_by_id = any(soup.find(id=re.compile(c, re.I)) for c in nav_selectors)

    if not has_nav and not has_nav_by_class and not has_nav_by_id:
        issues.append({
            "title": "No navigation menu detected",
            "description": "Could not find a primary navigation menu on the page.",
            "severity": "critical", "difficulty": "medium",
            "business_impact": "Users cannot easily browse the website, increasing bounce rate",
            "revenue_impact_pct": 15.0,
            "recommendation": "Add a clear, descriptive navigation menu to all pages",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for footer navigation
    footer = soup.find("footer")
    if footer:
        footer_links = footer.find_all("a")
        if len(footer_links) < 3:
            issues.append({
                "title": "Footer has minimal navigation links",
                "description": f"Footer only has {len(footer_links)} link(s).",
                "severity": "low", "difficulty": "easy",
                "business_impact": "Missed opportunity for secondary navigation and SEO",
                "recommendation": "Add footer links for important pages (About, Services, Contact, Privacy)",
                "fix_price_cents": 7900, "is_quick_fix": True,
            })
    else:
        issues.append({
            "title": "Missing footer section",
            "description": "No <footer> tag found. Footer provides important navigation context.",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Reduces usability and trust signals",
            "recommendation": "Add a footer with navigation links, contact info, and legal pages",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for breadcrumbs
    has_breadcrumbs = bool(soup.find(class_=re.compile(r"breadcrumb", re.I))) or bool(soup.find(attrs={"aria-label": re.compile(r"breadcrumb", re.I)}))
    if not has_breadcrumbs:
        issues.append({
            "title": "No breadcrumb navigation detected",
            "description": "Breadcrumbs help users understand their location in the site.",
            "severity": "low", "difficulty": "medium",
            "business_impact": "Reduces site usability, especially on deeper pages",
            "recommendation": "Add breadcrumb navigation to inner pages",
            "fix_price_cents": 7900, "is_quick_fix": False,
        })

    return issues


import re