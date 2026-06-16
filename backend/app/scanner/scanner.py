"""Core scanning engine that orchestrates the 17-category audit."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from app.models.models import AuditStatus, AuditCategory, Issue, IssueSeverity, FixDifficulty
from app.categories.registry import CATEGORY_SCANNERS

logger = logging.getLogger(__name__)


async def fetch_page(url: str) -> tuple[Optional[str], Optional[dict]]:
    """Fetch a single page and return (html, headers)."""
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url, headers={
                "User-Agent": "VelvetHourAudit/1.0 (Website Analyzer)"
            })
            resp.raise_for_status()
            return resp.text, dict(resp.headers)
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None, None


async def run_audit_scan(audit_id: str):
    """Orchestrate a full audit scan across all 17 categories."""
    from app.core.database import AsyncSessionLocal
    from sqlalchemy import select
    from app.models.models import Audit, Website, AuditCategory, Issue, IssueSeverity, FixDifficulty

    async with AsyncSessionLocal() as db:
        try:
            # Load audit
            result = await db.execute(select(Audit).where(Audit.id == audit_id))
            audit = result.scalar_one_or_none()
            if not audit:
                logger.error(f"Audit {audit_id} not found")
                return

            # Mark as running
            audit.status = AuditStatus.RUNNING
            audit.started_at = datetime.now(timezone.utc)
            await db.flush()

            # Load website
            web_result = await db.execute(select(Website).where(Website.id == audit.website_id))
            website = web_result.scalar_one()

            # Fetch homepage
            html, headers = await fetch_page(website.url)
            if not html:
                audit.status = AuditStatus.FAILED
                audit.error_message = "Unable to fetch website"
                await db.commit()
                return

            soup = BeautifulSoup(html, "lxml")

            # Run all category scanners
            all_issues = []
            category_scores = {}
            total_weight = 0
            weighted_score_sum = 0

            # Category weights (matching PRD)
            weights = {
                "mobile_responsiveness": 9,
                "page_speed": 9,
                "seo_fundamentals": 8,
                "local_seo": 7,
                "accessibility": 7,
                "user_experience": 7,
                "navigation": 6,
                "conversion_optimization": 8,
                "calls_to_action": 7,
                "contact_visibility": 6,
                "trust_signals": 6,
                "reviews_reputation": 4,
                "content_quality": 5,
                "image_optimization": 4,
                "security_basics": 3,
                "technical_issues": 2,
                "lead_generation": 2,
            }

            for scanner_name, scanner_func in CATEGORY_SCANNERS.items():
                try:
                    issues = await scanner_func(soup, html, headers, website.url)
                    category_score = calculate_category_score(issues)
                    weight = weights.get(scanner_name, 5)

                    # Store category score
                    cat = AuditCategory(
                        audit_id=audit.id,
                        category_name=scanner_name,
                        display_name=scanner_name.replace("_", " ").title(),
                        score=category_score,
                        issue_count=len(issues),
                        critical_count=sum(1 for i in issues if i.get("severity") == "critical"),
                        high_count=sum(1 for i in issues if i.get("severity") == "high"),
                        medium_count=sum(1 for i in issues if i.get("severity") == "medium"),
                        low_count=sum(1 for i in issues if i.get("severity") == "low"),
                        summary=f"Found {len(issues)} issue(s) in {scanner_name.replace('_', ' ').title()}",
                    )
                    db.add(cat)
                    category_scores[scanner_name] = category_score
                    total_weight += weight
                    weighted_score_sum += category_score * weight

                    # Store issues
                    for issue_data in issues:
                        issue = Issue(
                            audit_id=audit.id,
                            category_name=scanner_name,
                            title=issue_data.get("title", "Unknown issue"),
                            description=issue_data.get("description"),
                            severity=IssueSeverity(issue_data.get("severity", "low")),
                            difficulty=issue_data.get("difficulty"),
                            business_impact=issue_data.get("business_impact"),
                            revenue_impact_pct=issue_data.get("revenue_impact_pct"),
                            affected_element=issue_data.get("affected_element"),
                            recommendation=issue_data.get("recommendation"),
                            fix_preview=issue_data.get("fix_preview"),
                            fix_price_cents=issue_data.get("fix_price_cents"),
                            is_quick_fix=issue_data.get("is_quick_fix", False),
                        )
                        db.add(issue)
                        all_issues.append(issue_data)

                except Exception as e:
                    logger.error(f"Scanner {scanner_name} failed: {e}")
                    cat = AuditCategory(
                        audit_id=audit.id,
                        category_name=scanner_name,
                        display_name=scanner_name.replace("_", " ").title(),
                        score=0,
                        issue_count=0,
                        summary=f"Scanner error: {str(e)[:200]}",
                    )
                    db.add(cat)

            # Calculate overall score
            overall_score = round(weighted_score_sum / total_weight, 1) if total_weight > 0 else 0
            audit.overall_score = overall_score
            audit.page_count_scanned = 1  # Homepage only for MVP
            audit.status = AuditStatus.COMPLETE
            audit.completed_at = datetime.now(timezone.utc)
            audit.scan_metadata = {
                "pages_scanned": [website.url],
                "total_issues": len(all_issues),
                "category_scores": category_scores,
            }

            await db.commit()
            logger.info(f"Audit {audit_id} completed with score {overall_score}")

        except Exception as e:
            logger.error(f"Audit {audit_id} failed: {e}")
            try:
                audit.status = AuditStatus.FAILED
                audit.error_message = str(e)[:500]
                await db.commit()
            except Exception:
                pass


def calculate_category_score(issues: list[dict]) -> float:
    """Calculate score for a category (0-100) based on severity of issues."""
    severity_deductions = {
        "critical": 30,
        "high": 15,
        "medium": 7,
        "low": 3,
        "info": 0,
    }
    deductions = sum(severity_deductions.get(i.get("severity", "low"), 3) for i in issues)
    return max(0, round(min(100, 100 - deductions), 1))