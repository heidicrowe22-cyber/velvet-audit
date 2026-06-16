"""User Experience scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("user_experience")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check UX issues."""
    issues = []

    # Check for large paragraphs (wall of text)
    long_paras = [p for p in soup.find_all("p") if len(p.get_text(strip=True)) > 500]
    if long_paras:
        issues.append({
            "title": f"{len(long_paras)} paragraph(s) are too long",
            "description": "Long paragraphs (>500 chars) reduce readability on web.",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Visitors may skim past important content",
            "recommendation": "Break long paragraphs into shorter sections (2-3 sentences max)",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    # Check for sufficient whitespace (look at spacing between elements)
    # Heuristic: check if content is all crammed in one container
    main_content = soup.find(["main", "article", "div", "section"])
    if main_content:
        text_len = len(main_content.get_text(strip=True))
        # Check for inline styles that suggest poor spacing
        tight_spacing = any("margin: 0" in str(s.get("style", "")) or "padding: 0" in str(s.get("style", ""))
                          for s in soup.find_all(style=True))
        if tight_spacing:
            issues.append({
                "title": "Insufficient spacing between elements",
                "description": "Elements appear to have minimal margins/padding.",
                "severity": "low", "difficulty": "medium",
                "business_impact": "Content feels cramped, reducing readability",
                "recommendation": "Add adequate margins and padding to content sections",
                "fix_price_cents": 7900, "is_quick_fix": False,
            })

    # Check font size
    small_fonts = soup.find_all(style=re.compile(r'font-size:\s*(\d+)px'))
    for el in small_fonts:
        size_match = re.search(r'font-size:\s*(\d+)px', el.get("style", ""))
        if size_match and int(size_match.group(1)) < 14:
            issues.append({
                "title": "Text smaller than 14px detected",
                "description": f"Text uses {size_match.group(1)}px font which is hard to read.",
                "severity": "medium", "difficulty": "easy",
                "business_impact": "Difficult to read, especially on mobile",
                "recommendation": "Use minimum 16px font size for body text",
                "fix_price_cents": 7900, "is_quick_fix": True,
            })
            break

    return issues


import re