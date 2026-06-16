"""Lead Generation scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("lead_generation")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check lead generation issues."""
    issues = []

    # Check for newsletter/email signup
    email_keywords = r'newsletter|subscribe|sign.?up|email.*updates|get.*updates|mailing.*list'
    has_signup = bool(re.search(email_keywords, html, re.I))
    if not has_signup:
        issues.append({
            "title": "No email/newsletter signup found",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "No way to capture leads who aren't ready to buy yet",
            "revenue_impact_pct": 8.0,
            "recommendation": "Add an email newsletter signup form to capture visitor emails",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for lead magnets
    magnet_keywords = r'free.*(guide|ebook|checklist|template|consultation|quote|estimate|download|pdf)'
    has_lead_magnet = bool(re.search(magnet_keywords, html, re.I))
    if not has_lead_magnet:
        issues.append({
            "title": "No lead magnet or free offer detected",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Free offers convert 3-5x better than direct sales pitches",
            "recommendation": "Offer a free guide, checklist, or consultation to capture leads",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for booking/scheduling integration
    booking_terms = r'book.*(now|appointment|online)|schedule|calendar|reserve|book.*demo|free.*consult'
    has_booking = bool(re.search(booking_terms, html, re.I))
    if not has_booking:
        issues.append({
            "title": "No booking or scheduling option",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Service businesses without online booking lose 30% of potential clients",
            "revenue_impact_pct": 10.0,
            "recommendation": "Add online booking/scheduling integration (Calendly, Acuity, etc.)",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    return issues


import re