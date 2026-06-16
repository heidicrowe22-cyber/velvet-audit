"""Trust Signals scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("trust_signals")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check trust signal issues."""
    issues = []

    # Check for privacy policy
    has_privacy = bool(re.search(r'privacy|privacy.policy|gdpr|data.protection', html, re.I))
    if not has_privacy:
        issues.append({
            "title": "No privacy policy found",
            "severity": "high", "difficulty": "easy",
            "business_impact": "Legal requirement for most businesses. Reduces user trust.",
            "revenue_impact_pct": 5.0,
            "recommendation": "Add a privacy policy page and link it in the footer",
            "fix_price_cents": 7900, "is_quick_fix": False,
        })

    # Check for terms of service
    has_terms = bool(re.search(r'terms|terms.of.service|terms.conditions|tos', html, re.I))
    if not has_terms:
        issues.append({
            "title": "No terms of service found",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Legal protection vulnerability. Reduces professional appearance.",
            "recommendation": "Add terms of service page with clear business policies",
            "fix_price_cents": 7900, "is_quick_fix": False,
        })

    # Check for about page
    about_links = soup.find_all("a", href=re.compile(r"about|about.us|our.story|who.we.are", re.I))
    if not about_links:
        issues.append({
            "title": "No About page link found",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Users want to know who they're doing business with",
            "recommendation": "Add an About page with team info, mission, and story",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    # Check for trust badges/seals
    trust_keywords = r'ssl|secure|verified|trusted|bbb|norton|mcafee|trustpilot|better.business'
    has_trust_badge = bool(re.search(trust_keywords, html, re.I))
    if not has_trust_badge:
        issues.append({
            "title": "No trust badges or security seals detected",
            "severity": "low", "difficulty": "medium",
            "business_impact": "Trust badges can increase conversion rates by 15-30%",
            "recommendation": "Add relevant trust badges (SSL, BBB, payment logos) near CTAs",
            "fix_price_cents": 7900, "is_quick_fix": False,
        })

    return issues


import re