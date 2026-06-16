"""17 Category audit scanners registry."""

from typing import Callable, Coroutine

# Each scanner is an async function:
#   async def scan(soup, html, headers, url) -> list[dict]
# where soup is BeautifulSoup object, html is raw HTML string,
# headers is response headers dict, url is the website URL.
# Returns a list of issue dicts.

CATEGORY_SCANNERS: dict[str, Callable] = {}

def register_scanner(name: str):
    """Decorator to register a category scanner."""
    def decorator(func):
        CATEGORY_SCANNERS[name] = func
        return func
    return decorator


# Import all scanners to register them
from app.categories import (
    mobile_responsiveness,
    page_speed,
    seo_fundamentals,
    local_seo,
    accessibility,
    user_experience,
    navigation,
    conversion_optimization,
    calls_to_action,
    contact_visibility,
    trust_signals,
    reviews_reputation,
    content_quality,
    image_optimization,
    security_basics,
    technical_issues,
    lead_generation,
)

__all__ = ["CATEGORY_SCANNERS", "register_scanner"]