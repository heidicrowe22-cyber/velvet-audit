"""Reviews & Reputation scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("reviews_reputation")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check reviews and reputation issues."""
    issues = []

    # Check for review schema markup
    has_review_schema = False
    for script in soup.find_all("script", type="application/ld+json"):
        import json
        try:
            data = json.loads(script.string) if script.string else {}
            if isinstance(data, dict):
                if data.get("@type") in ("Review", "AggregateRating", "Product", "LocalBusiness"):
                    if "aggregateRating" in str(data) or "review" in str(data).lower():
                        has_review_schema = True
                        break
        except (json.JSONDecodeError, AttributeError):
            continue

    if not has_review_schema:
        issues.append({
            "title": "Missing review/rating schema markup",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Search results won't show star ratings, reducing CTR by ~20%",
            "revenue_impact_pct": 5.0,
            "recommendation": "Add AggregateRating or Review schema to display star ratings in search results",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for displayed reviews/testimonials
    review_keywords = r'testimonial|review|rating|stars?|what.*clients?.*say|success.stories'
    has_reviews = bool(re.search(review_keywords, html, re.I))
    if not has_reviews:
        issues.append({
            "title": "No customer reviews or testimonials displayed",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "85% of users trust online reviews as much as personal recommendations",
            "recommendation": "Add customer testimonials or review widget to the website",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for third-party review platform links
    review_platforms = r'google.*review|yelp|trustpilot|facebook.*review|bbb\.org'
    has_platform = bool(re.search(review_platforms, html, re.I))
    if not has_platform:
        issues.append({
            "title": "No links to third-party review platforms",
            "severity": "low", "difficulty": "easy",
            "business_impact": "Missed opportunity to leverage external social proof",
            "recommendation": "Add links to Google Reviews, Yelp, or Trustpilot profiles",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    return issues


import re