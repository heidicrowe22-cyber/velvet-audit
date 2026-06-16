"""Accessibility (a11y) scanner - WCAG 2.1 AA checks."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("accessibility")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check accessibility issues."""
    issues = []

    # Missing alt text on images
    imgs_no_alt = soup.find_all("img", alt=False)
    imgs_empty_alt = soup.find_all("img", alt="")
    if imgs_no_alt:
        issues.append({
            "title": f"{len(imgs_no_alt)} image(s) missing alt text",
            "description": "Images without alt text are invisible to screen readers.",
            "severity": "high", "difficulty": "easy",
            "business_impact": "WCAG 2.1 AA violation. Excludes visually impaired users.",
            "revenue_impact_pct": 2.0,
            "recommendation": "Add descriptive alt text to all images",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    # Check html lang attribute
    html_tag = soup.find("html")
    if html_tag and not html_tag.get("lang"):
        issues.append({
            "title": "Missing lang attribute on <html>",
            "severity": "high", "difficulty": "easy",
            "business_impact": "Screen readers can't determine page language",
            "recommendation": 'Add lang="en" (or appropriate language) to <html> tag',
            "fix_preview": '<html lang="en">',
            "fix_price_cents": 2900, "is_quick_fix": True,
        })

    # Check form inputs for labels
    inputs = soup.find_all(["input", "textarea", "select"])
    unlabeled = []
    for inp in inputs:
        if inp.get("type") in ("hidden", "submit", "button", "reset"):
            continue
        inp_id = inp.get("id")
        if inp_id:
            label = soup.find("label", attrs={"for": inp_id})
            if label:
                continue
        # Check for aria-label
        if inp.get("aria-label"):
            continue
        # Check for wrapping label
        parent_label = inp.find_parent("label")
        if parent_label:
            continue
        unlabeled.append(inp)

    if unlabeled:
        issues.append({
            "title": f"{len(unlabeled)} form field(s) missing labels",
            "description": "Form inputs need associated labels for accessibility.",
            "severity": "high", "difficulty": "medium",
            "business_impact": "Screen reader users cannot use forms. WCAG violation.",
            "revenue_impact_pct": 3.0,
            "recommendation": "Add <label> elements or aria-label attributes to all form fields",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check color contrast (heuristic - look for inline color styles)
    color_styles = [s for s in (soup.find_all(style=True)) if "color:" in s.get("style", "")]
    if not color_styles:
        # No inline colors - still worth mentioning
        issues.append({
            "title": "Unable to verify color contrast",
            "description": "No inline color styles detected. Color contrast should be checked manually.",
            "severity": "info", "difficulty": "medium",
            "business_impact": "Poor contrast affects readability for 8% of male users (color blindness)",
            "recommendation": "Ensure text/background contrast ratio is at least 4.5:1",
            "fix_price_cents": 7900, "is_quick_fix": False,
        })

    return issues