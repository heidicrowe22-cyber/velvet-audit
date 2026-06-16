"""Local SEO scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("local_seo")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check local SEO issues."""
    issues = []

    # Check for LocalBusiness schema
    has_local_business = False
    for script in soup.find_all("script", type="application/ld+json"):
        import json
        try:
            data = json.loads(script.string) if script.string else {}
            if isinstance(data, dict):
                if data.get("@type") == "LocalBusiness":
                    has_local_business = True
                    break
                if isinstance(data.get("@graph"), list):
                    for item in data["@graph"]:
                        if item.get("@type") == "LocalBusiness":
                            has_local_business = True
                            break
        except (json.JSONDecodeError, AttributeError):
            continue

    if not has_local_business:
        issues.append({
            "title": "Missing LocalBusiness schema markup",
            "description": "No LocalBusiness structured data found. Helps search engines understand business details.",
            "severity": "high", "difficulty": "medium",
            "business_impact": "Reduces visibility in local search results and knowledge panels",
            "revenue_impact_pct": 10.0,
            "recommendation": "Add LocalBusiness schema with name, address, phone, and hours",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for NAP (Name, Address, Phone) consistency
    has_phone = bool(soup.find(string=re.compile(r'[\+\d\-\(\)\s]{10,}')))
    has_address = bool(soup.find(string=re.compile(r'(street|ave|blvd|road|drive|suite|#\d)', re.I)))

    if not has_phone:
        issues.append({
            "title": "Phone number not clearly visible",
            "description": "No obvious phone number found in the page content.",
            "severity": "high", "difficulty": "easy",
            "business_impact": "Customers can't easily call the business",
            "revenue_impact_pct": 7.0,
            "recommendation": "Add phone number prominently (preferably in header/footer)",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    if not has_address:
        issues.append({
            "title": "Physical address not found on page",
            "description": "No obvious street address found. Local SEO requires visible address.",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Hampers local search ranking and customer trust",
            "recommendation": "Add physical business address to website footer",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Check for Google Business Profile link
    has_gbp = "google.com/business" in html.lower() or "google.com/maps" in html.lower()
    if not has_gbp:
        issues.append({
            "title": "No Google Business Profile link found",
            "severity": "low", "difficulty": "easy",
            "business_impact": "Missed opportunity for social proof and local SEO signals",
            "recommendation": "Add a link to your Google Business Profile on the contact page",
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    return issues


import re