"""Security Basics scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("security_basics")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check security issues."""
    issues = []

    # Check if page is served over HTTPS
    if not url.startswith("https://"):
        issues.append({
            "title": "Website not using HTTPS",
            "severity": "critical", "difficulty": "medium",
            "business_impact": "Security warning in browsers. Google ranks HTTPS higher.",
            "revenue_impact_pct": 20.0,
            "recommendation": "Install an SSL certificate and redirect HTTP to HTTPS",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for mixed content (HTTP resources on HTTPS page)
    if url.startswith("https://"):
        http_srcs = re.findall(r'src="http://[^"]+|href="http://[^"]+', html)
        if http_srcs:
            issues.append({
                "title": f"Mixed content detected ({len(http_srcs)} HTTP resource(s))",
                "description": "HTTPS page loading HTTP resources causes browser warnings.",
                "severity": "high", "difficulty": "medium",
                "business_impact": "Browsers may block mixed content, breaking page features",
                "recommendation": "Replace all HTTP resource URLs with HTTPS equivalents",
                "fix_price_cents": 7900, "is_quick_fix": True,
            })

    # Check CSP header
    csp = headers.get("content-security-policy", "").lower() if headers else ""
    if not csp:
        issues.append({
            "title": "No Content Security Policy (CSP) header",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "Vulnerable to XSS attacks. Modern security best practice.",
            "recommendation": "Implement a Content Security Policy header",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for form action security
    for form in soup.find_all("form"):
        action = form.get("action", "")
        if action and not action.startswith(("https://", "/", "#")):
            issues.append({
                "title": "Form submits to non-HTTPS URL",
                "description": f"Form action '{action}' is not secure.",
                "severity": "critical", "difficulty": "easy",
                "business_impact": "User data transmitted insecurely. Trust/legal risk.",
                "recommendation": "Change form action to use HTTPS or relative path",
                "fix_price_cents": 7900, "is_quick_fix": True,
            })
            break

    return issues


import re