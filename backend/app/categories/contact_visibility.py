"""Contact Visibility scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("contact_visibility")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check contact visibility issues."""
    issues = []

    # Check for contact page link
    contact_links = soup.find_all("a", href=re.compile(r"contact|get-in-touch|reach-us", re.I))
    if not contact_links:
        issues.append({
            "title": "No contact page link found",
            "severity": "critical", "difficulty": "easy",
            "business_impact": "Customers can't find how to reach you - major trust issue",
            "revenue_impact_pct": 18.0,
            "recommendation": "Add a 'Contact' link in the navigation and a contact form",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    # Check for phone number (click-to-call on mobile)
    phone_pattern = r'(tel:|[\+\d][\d\s\-\(\)]{7,}\d)'
    has_phone = bool(re.search(phone_pattern, html))

    if has_phone:
        has_tel_link = 'href="tel:' in html.lower() or "href='tel:" in html.lower()
        if not has_tel_link:
            issues.append({
                "title": "Phone number not clickable on mobile",
                "description": "Phone number found but not linked with tel: protocol.",
                "severity": "high", "difficulty": "easy",
                "business_impact": "Mobile users cannot tap-to-call, reducing conversions by 20%",
                "revenue_impact_pct": 8.0,
                "recommendation": "Wrap phone numbers in <a href='tel:+1234567890'> tags",
                "fix_price_cents": 2900, "is_quick_fix": True,
            })
    else:
        issues.append({
            "title": "No phone number found on the website",
            "severity": "high", "difficulty": "easy",
            "business_impact": "Customers may leave to find a competitor they can call",
            "revenue_impact_pct": 10.0,
            "recommendation": "Add phone number to header/footer prominently",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Check for contact form
    has_form = len(soup.find_all("form")) > 0
    if not has_form:
        issues.append({
            "title": "No contact form on the website",
            "severity": "high", "difficulty": "medium",
            "business_impact": "Many users prefer forms over email or phone calls",
            "revenue_impact_pct": 8.0,
            "recommendation": "Add a contact form with name, email, and message fields",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    return issues


import re