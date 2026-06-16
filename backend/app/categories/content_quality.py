"""Content Quality scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("content_quality")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check content quality issues."""
    issues = []

    # Get all text content
    body = soup.find("body")
    if not body:
        return issues

    text_content = body.get_text(separator=" ", strip=True)
    word_count = len(text_content.split())

    if word_count < 300:
        issues.append({
            "title": f"Very thin content ({word_count} words)",
            "severity": "high", "difficulty": "medium",
            "business_impact": "Thin content ranks poorly in search and fails to engage visitors",
            "revenue_impact_pct": 12.0,
            "recommendation": "Expand content to at least 500 words with valuable information",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })
    elif word_count < 500:
        issues.append({
            "title": f"Content could be expanded ({word_count} words)",
            "severity": "low", "difficulty": "medium",
            "business_impact": "More comprehensive content improves engagement and SEO",
            "recommendation": "Add more detail to better serve user intent",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for clear value proposition in first 200 chars
    first_200 = text_content[:200].lower()
    vp_keywords = r'(we (are|provide|offer|specialize)|our (mission|goal|service)|get (started|a quote|your))'
    has_value_prop = bool(re.search(vp_keywords, first_200))
    if not has_value_prop:
        issues.append({
            "title": "Value proposition not immediately clear",
            "severity": "high", "difficulty": "medium",
            "business_impact": "Visitors should understand your offering within 5 seconds",
            "revenue_impact_pct": 15.0,
            "recommendation": "Add a clear value proposition above the fold explaining what you do",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for readability (Flesch heuristic - avg sentence length)
    sentences = [s.strip() for s in text_content.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    if sentences:
        avg_words = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_words > 25:
            issues.append({
                "title": "Sentences are too long on average",
                "description": f"Average sentence length: {avg_words:.0f} words (target: 15-20).",
                "severity": "low", "difficulty": "medium",
                "business_impact": "Long sentences reduce readability, especially on mobile",
                "recommendation": "Break long sentences into shorter, more readable ones",
                "fix_price_cents": 7900, "is_quick_fix": True,
            })

    return issues


import re