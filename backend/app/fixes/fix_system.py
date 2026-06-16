"""Fix system - pricing, estimation, and implementation tracking."""

FIX_TYPES = {
    "quick_fix": {
        "name": "Quick Fix",
        "price_cents": 2900,
        "estimated_days": 1,
        "description": "Simple text/code change for a single issue",
    },
    "standard_fix": {
        "name": "Standard Fix",
        "price_cents": 7900,
        "estimated_days": 2,
        "description": "Moderate complexity fix for one category's issues",
    },
    "category_fix": {
        "name": "Category Fix",
        "price_cents": 14900,
        "estimated_days": 3,
        "description": "Full optimization of one audit category",
    },
    "bundle_fix": {
        "name": "Bundle Fix",
        "price_cents": 29900,
        "estimated_days": 5,
        "description": "3-5 related fixes across multiple categories",
    },
}

PLATFORM_FIX_METHODS = {
    "wordpress": "WordPress Admin / Plugin / Direct DB",
    "shopify": "Shopify Theme Editor / API",
    "wix": "Wix Editor",
    "squarespace": "Squarespace Editor / API",
    "webflow": "Webflow Designer / Custom Code",
    "godaddy": "GoDaddy Website Builder",
    "custom": "Direct HTML/CSS/JS via FTP or Git",
}


def get_fix_estimate(issues: list[dict]) -> dict:
    """Estimate cost and effort for a set of issues."""
    critical_count = sum(1 for i in issues if i.get("severity") == "critical")
    high_count = sum(1 for i in issues if i.get("severity") == "high")
    total_issues = len(issues)

    if total_issues == 0:
        return {"package": "none", "price_cents": 0, "days": 0}

    if total_issues <= 2 and critical_count == 0:
        return dict(FIX_TYPES["quick_fix"])
    elif total_issues <= 5 and critical_count <= 1:
        return dict(FIX_TYPES["standard_fix"])
    elif total_issues <= 10:
        return dict(FIX_TYPES["category_fix"])
    else:
        return dict(FIX_TYPES["bundle_fix"])


def create_implementation_task(order_id: str, platform: str, issues: list[dict]) -> dict:
    """Create an implementation task for the fix pipeline."""
    method = PLATFORM_FIX_METHODS.get(platform, PLATFORM_FIX_METHODS["custom"])
    return {
        "order_id": order_id,
        "platform": platform,
        "fix_method": method,
        "issue_count": len(issues),
        "status": "queued",
    }