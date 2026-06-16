"""Conversion Optimization scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("conversion_optimization")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check conversion optimization issues."""
    issues = []

    forms = soup.find_all("form")
    if forms:
        for form in forms:
            input_count = len(form.find_all(["input", "textarea", "select"]))
            if input_count > 5:
                issues.append({
                    "title": f"Form has {input_count} fields (may be too many)",
                    "severity": "medium", "difficulty": "medium",
                    "business_impact": "Each additional form field reduces conversion by ~5%",
                    "revenue_impact_pct": 10.0,
                    "recommendation": "Reduce form fields to essentials (name, email, message)",
                    "fix_price_cents": 14900, "is_quick_fix": False,
                })
                break

    # Check for landing page structure
    has_hero = bool(soup.find(class_=re.compile(r"hero|banner|header", re.I)) or soup.find(id=re.compile(r"hero|banner", re.I)))
    if not has_hero:
        issues.append({
            "title": "No hero/banner section detected",
            "description": "A hero section above the fold communicates value proposition.",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Visitors may not understand your value within seconds",
            "recommendation": "Add a hero section with clear value proposition and CTA",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for social proof elements
    has_testimonials = bool(soup.find(string=re.compile(r"testimonial|review|what.*client.*say|customer.*story", re.I)))
    if not has_testimonials:
        issues.append({
            "title": "No testimonials or social proof found",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Social proof can boost conversions by up to 34%",
            "recommendation": "Add testimonials, case studies, or client logos to build trust",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    return issues


import re