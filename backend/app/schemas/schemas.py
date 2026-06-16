"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field


# ─── Auth ──────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None
    company: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    company: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ─── Websites ──────────────────────────────────────────────────

class WebsiteCreate(BaseModel):
    url: str = Field(..., max_length=2048)
    name: Optional[str] = None
    platform: Optional[str] = None


class WebsiteResponse(BaseModel):
    id: str
    url: str
    domain: str
    platform: Optional[str] = None
    name: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Audits ────────────────────────────────────────────────────

class AuditCreate(BaseModel):
    website_url: str = Field(..., max_length=2048)


class AuditCategoryScore(BaseModel):
    category_name: str
    display_name: str
    score: Optional[float] = None
    issue_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    summary: Optional[str] = None


class IssueResponse(BaseModel):
    id: str
    category_name: str
    title: str
    description: Optional[str] = None
    severity: str
    difficulty: Optional[str] = None
    business_impact: Optional[str] = None
    revenue_impact_pct: Optional[float] = None
    affected_element: Optional[str] = None
    recommendation: Optional[str] = None
    fix_preview: Optional[str] = None
    fix_price_cents: Optional[int] = None
    is_quick_fix: bool = False

    model_config = {"from_attributes": True}


class AuditStatusResponse(BaseModel):
    id: str
    website_id: str
    status: str
    overall_score: Optional[float] = None
    page_count_scanned: int = 0
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditResponse(AuditStatusResponse):
    categories: list[AuditCategoryScore] = []
    issues: list[IssueResponse] = []


# ─── Fixes ─────────────────────────────────────────────────────

class FixPackageResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price_cents: int
    estimated_days: Optional[int] = None
    is_bundle: bool = False

    model_config = {"from_attributes": True}


class FixEstimateRequest(BaseModel):
    audit_id: str
    issue_ids: list[str]


class FixEstimateResponse(BaseModel):
    total_cents: int
    packages: list[FixPackageResponse]
    estimated_days: int


# ─── Orders ────────────────────────────────────────────────────

class OrderItemResponse(BaseModel):
    id: str
    description: str
    price_cents: int

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    audit_id: str
    fix_package_ids: list[str] = []


class OrderResponse(BaseModel):
    id: str
    status: str
    total_cents: int
    items: list[OrderItemResponse] = []
    created_at: datetime
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Implementations ───────────────────────────────────────────

class ImplementationResponse(BaseModel):
    id: str
    order_id: str
    status: str
    platform: Optional[str] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


# ─── Reports ───────────────────────────────────────────────────

class ReportResponse(BaseModel):
    id: str
    audit_id: str
    overall_score: float
    category_scores: dict
    issue_summary: dict
    top_issues: Optional[list] = None
    quick_wins: Optional[list] = None
    summary_text: Optional[str] = None
    generated_at: datetime

    model_config = {"from_attributes": True}