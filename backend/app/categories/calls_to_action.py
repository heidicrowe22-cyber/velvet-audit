"""Calls to Action scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("calls_to_action")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check CTA issues."""
    issues = []

    # Find button/CTA elements
    ctas = soup.find_all(["button", "a"], class_=re.compile(r"btn|cta|button|action", re.I))
    if not ctas:
        ctas = soup.find_all(["button", "a"], href=re.compile(r"contact|signup|register|book|schedule|quote|order|buy|get", re.I))

    if not ctas:
        ctas = soup.find_all(["button"])

    if not ctas:
        issues.append({
            "title": "No clear call-to-action buttons found",
            "severity": "critical", "difficulty": "medium",
            "business_impact": "Visitors don't know what action to take next, losing conversions",
            "revenue_impact_pct": 25.0,
            "recommendation": "Add prominent CTAs: 'Get Started', 'Book Now', 'Get a Quote'",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })
    else:
        # Check CTA copy quality
        weak_ctas = ["submit", "click here", "go", "enter", "send"]
        for cta in ctas:
            cta_text = cta.get_text(strip=True).lower()
            if cta_text in weak_ctas or any(w == cta_text for w in weak_ctas):
                issues.append({
                    "title": "Weak CTA button copy",
                    "description": f"Button '{cta.get_text(strip=True)}' is not compelling.",
                    "severity": "medium", "difficulty": "easy",
                    "business_impact": "Weak CTAs reduce click-through rates by 30-50%",
                    "revenue_impact_pct": 8.0,
                    "recommendation": "Use action-oriented CTAs: 'Get My Free Quote', 'Book Your Appointment'",
                    "fix_price_cents": 2900, "is_quick_fix": True,
                })
                break

    # Check if CTAs are above the fold (heuristic: early in HTML)
    if ctas:
        first_cta = ctas[0]
        if first_cta.sourcepos and first_cta.sourcepos > 5000:
            issues.append({
                "title": "CTA appears below the fold",
                "severity": "high", "difficulty": "medium",
                "business_impact": "Users may not scroll to find your CTA",
                "revenue_impact_pct": 12.0,
                "recommendation": "Move primary CTA above the fold (visible without scrolling)",
                "fix_price_cents": 14900, "is_quick_fix": False,
            })

    return issues


import re