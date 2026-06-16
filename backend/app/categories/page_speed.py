"""Page Speed scanner."""

import re
from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("page_speed")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check page speed issues."""
    issues = []

    # Check for render-blocking CSS/JS in head
    head = soup.find("head")
    if head:
        inline_styles = head.find_all("link", rel="stylesheet")
        render_blocking_scripts = [s for s in head.find_all("script") if not s.get("async") and not s.get("defer")]

        if inline_styles:
            issues.append({
                "title": f"{len(inline_styles)} render-blocking stylesheet(s) detected",
                "description": "CSS files linked in <head> block rendering. Consider inlining critical CSS.",
                "severity": "high",
                "difficulty": "medium",
                "business_impact": "Increases First Contentful Paint by 300-500ms",
                "revenue_impact_pct": 5.0,
                "affect_element": "<head> section",
                "recommendation": "Inline critical CSS and defer non-critical stylesheets",
                "fix_price_cents": 14900,
                "is_quick_fix": False,
            })

        if render_blocking_scripts:
            issues.append({
                "title": f"{len(render_blocking_scripts)} render-blocking script(s) in <head>",
                "description": "Scripts in <head> block HTML parsing. Add async or defer attributes.",
                "severity": "medium",
                "difficulty": "easy",
                "business_impact": "Delays page rendering by script download + execution time",
                "revenue_impact_pct": 3.0,
                "recommendation": "Add 'async' or 'defer' attributes to non-critical scripts",
                "fix_price_cents": 7900,
                "is_quick_fix": True,
            })

    # Check for images without explicit dimensions
    imgs_no_dim = soup.find_all("img")
    for img in imgs_no_dim:
        if not img.get("width") and not img.get("height") and not img.get("loading"):
            issues.append({
                "title": "Images missing width/height attributes",
                "description": f"Image '{img.get('alt', img.get('src', 'unknown'))[:50]}' lacks dimension attributes, causing layout shifts.",
                "severity": "medium",
                "difficulty": "easy",
                "business_impact": "Increases Cumulative Layout Shift (CLS), harming user experience",
                "revenue_impact_pct": 2.0,
                "affected_element": img.get("src", "")[:100],
                "recommendation": "Add width and height attributes to all images",
                "fix_price_cents": 7900,
                "is_quick_fix": True,
            })
            break

    # Check for lazy loading
    has_lazy = html.count('loading="lazy"') > 0 or html.count("loading='lazy'") > 0
    total_imgs = len(soup.find_all("img"))
    if total_imgs > 3 and not has_lazy:
        issues.append({
            "title": "Lazy loading not enabled for images",
            "description": f"Page has {total_imgs} images but none use lazy loading.",
            "severity": "medium",
            "difficulty": "easy",
            "business_impact": "All images load on page start, increasing initial page weight",
            "recommendation": "Add loading='lazy' to below-the-fold images",
            "fix_price_cents": 7900,
            "is_quick_fix": True,
        })

    # Check for large inline images (heuristic: check data URIs)
    data_uris = re.findall(r'data:image/[^;]+;base64,[^\'"]+', html)
    if data_uris:
        issues.append({
            "title": "Large inline base64 images detected",
            "description": f"Found {len(data_uris)} base64 encoded images which bloat HTML size.",
            "severity": "low",
            "difficulty": "medium",
            "business_impact": "Increases page weight and blocks rendering",
            "recommendation": "Replace base64 images with external image files",
            "fix_price_cents": 7900,
            "is_quick_fix": False,
        })

    return issues