"""Image Optimization scanner."""

from bs4 import BeautifulSoup
from app.categories import register_scanner


@register_scanner("image_optimization")
async def scan(soup: BeautifulSoup, html: str, headers: dict, url: str) -> list[dict]:
    """Check image optimization issues."""
    issues = []

    images = soup.find_all("img")
    if not images:
        issues.append({
            "title": "No images found on the page",
            "severity": "info", "difficulty": "medium",
            "business_impact": "Images improve engagement and conversion rates",
            "recommendation": "Add relevant images to improve visual appeal and engagement",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })
        return issues

    # Check for alt text
    no_alt = [img for img in images if not img.get("alt")]
    if no_alt:
        issues.append({
            "title": f"{len(no_alt)} image(s) missing alt text",
            "description": "Alt text improves accessibility and image SEO.",
            "severity": "high", "difficulty": "easy",
            "business_impact": "Missed SEO opportunity. WCAG accessibility violation.",
            "revenue_impact_pct": 3.0,
            "recommendation": "Add descriptive alt text to all images",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    # Check for WebP format
    total_imgs = len(images)
    webp_imgs = len([img for img in images if img.get("src", "").lower().endswith(".webp")])
    if total_imgs > 2 and webp_imgs < total_imgs * 0.5:
        issues.append({
            "title": "Not using modern image formats (WebP)",
            "description": f"Using {total_imgs - webp_imgs} non-WebP image(s).",
            "severity": "medium", "difficulty": "medium",
            "business_impact": "WebP reduces image size by 25-35% without quality loss",
            "recommendation": "Convert images to WebP format and serve with fallbacks",
            "fix_price_cents": 14900, "is_quick_fix": False,
        })

    # Check for lazy loading
    lazy_count = len([img for img in images if img.get("loading") == "lazy"])
    imgs_below_top = len(images) - 1  # Exclude first image as hero
    if imgs_below_top > 0 and lazy_count < imgs_below_top:
        issues.append({
            "title": "Lazy loading not fully implemented",
            "description": f"Only {lazy_count} of {len(images)} images use lazy loading.",
            "severity": "medium", "difficulty": "easy",
            "business_impact": "Below-fold images load unnecessarily, slowing initial page load",
            "recommendation": "Add loading='lazy' to all below-the-fold images",
            "fix_price_cents": 7900, "is_quick_fix": True,
        })

    return issues