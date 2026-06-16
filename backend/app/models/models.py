"""Complete database schema for Velvet Hour Audit."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime,
    ForeignKey, JSON, Enum as SAEnum, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


def generate_uuid():
    return str(uuid.uuid4())


def utcnow():
    return datetime.now(timezone.utc)


# ─── Enums ─────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    AGENCY = "agency"


class AuditStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class IssueSeverity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FixDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class ImplementationStatus(str, enum.Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    QA_REVIEW = "qa_review"
    COMPLETED = "completed"
    FAILED = "failed"


class SubscriptionTier(str, enum.Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# ─── Models ────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    role = Column(SAEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    stripe_customer_id = Column(String(255), nullable=True)

    # Relationships
    websites = relationship("Website", back_populates="user")
    orders = relationship("Order", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class Website(Base):
    __tablename__ = "websites"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    url = Column(String(2048), nullable=False)
    domain = Column(String(255), nullable=False, index=True)
    platform = Column(String(100), nullable=True)  # wordpress, shopify, wix, squarespace, webflow, godaddy, custom
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="websites")
    audits = relationship("Audit", back_populates="website")
    platform_tokens = relationship("PlatformToken", back_populates="website")

    Index("idx_websites_user_id", "user_id")
    Index("idx_websites_domain", "domain")


class Audit(Base):
    __tablename__ = "audits"

    id = Column(String, primary_key=True, default=generate_uuid)
    website_id = Column(String, ForeignKey("websites.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(SAEnum(AuditStatus), default=AuditStatus.PENDING, nullable=False)
    overall_score = Column(Float, nullable=True)
    page_count_scanned = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Scan metadata
    scan_metadata = Column(JSON, nullable=True)  # e.g., {"pages_scanned": ["/", "/about"], "browser": "chromium"}

    # Relationships
    website = relationship("Website", back_populates="audits")
    user = relationship("User")
    categories = relationship("AuditCategory", back_populates="audit", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="audit", cascade="all, delete-orphan")
    report_snapshots = relationship("ReportSnapshot", back_populates="audit", cascade="all, delete-orphan")


class AuditCategory(Base):
    __tablename__ = "audit_categories"

    id = Column(String, primary_key=True, default=generate_uuid)
    audit_id = Column(String, ForeignKey("audits.id"), nullable=False, index=True)
    category_name = Column(String(100), nullable=False)  # e.g., "mobile_responsiveness"
    display_name = Column(String(255), nullable=False)  # e.g., "Mobile Responsiveness"
    score = Column(Float, nullable=True)
    issue_count = Column(Integer, default=0, nullable=False)
    critical_count = Column(Integer, default=0, nullable=False)
    high_count = Column(Integer, default=0, nullable=False)
    medium_count = Column(Integer, default=0, nullable=False)
    low_count = Column(Integer, default=0, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    audit = relationship("Audit", back_populates="categories")

    Index("idx_audit_categories_audit", "audit_id")


class Issue(Base):
    __tablename__ = "issues"

    id = Column(String, primary_key=True, default=generate_uuid)
    audit_id = Column(String, ForeignKey("audits.id"), nullable=False, index=True)
    category_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(SAEnum(IssueSeverity), nullable=False)
    difficulty = Column(SAEnum(FixDifficulty), nullable=True)
    business_impact = Column(String(500), nullable=True)
    revenue_impact_pct = Column(Float, nullable=True)  # Estimated % revenue impact
    affected_element = Column(String(500), nullable=True)  # e.g., CSS selector or URL
    recommendation = Column(Text, nullable=True)
    fix_preview = Column(Text, nullable=True)  # Code/text snippet showing the fix
    fix_price_cents = Column(Integer, nullable=True)  # Price in cents for fixing this issue
    fix_package_id = Column(String, ForeignKey("fix_packages.id"), nullable=True)
    is_quick_fix = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    audit = relationship("Audit", back_populates="issues")
    fix_package = relationship("FixPackage")

    Index("idx_issues_audit", "audit_id")
    Index("idx_issues_category", "audit_id", "category_name")


class FixPackage(Base):
    __tablename__ = "fix_packages"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)  # e.g., "Quick Fix", "Standard Fix"
    description = Column(Text, nullable=True)
    price_cents = Column(Integer, nullable=False)
    estimated_hours = Column(Float, nullable=True)
    estimated_days = Column(Integer, nullable=True)
    is_bundle = Column(Boolean, default=False, nullable=False)
    max_issues = Column(Integer, nullable=True)
    categories = Column(JSON, nullable=True)  # List of category names this package covers
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Default fix packages
    FIX_TYPES = {
        "quick_fix": {"name": "Quick Fix", "price_cents": 2900, "days": 1},
        "standard_fix": {"name": "Standard Fix", "price_cents": 7900, "days": 2},
        "category_fix": {"name": "Category Fix", "price_cents": 14900, "days": 3},
        "bundle_fix": {"name": "Bundle Fix", "price_cents": 29900, "days": 5},
    }


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    audit_id = Column(String, ForeignKey("audits.id"), nullable=True, index=True)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_cents = Column(Integer, nullable=False)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    stripe_session_id = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    implementations = relationship("Implementation", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False, index=True)
    fix_package_id = Column(String, ForeignKey("fix_packages.id"), nullable=True)
    issue_id = Column(String, ForeignKey("issues.id"), nullable=True)
    description = Column(String(500), nullable=False)
    price_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")


class Implementation(Base):
    __tablename__ = "implementations"

    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False, index=True)
    audit_id = Column(String, ForeignKey("audits.id"), nullable=True)
    issue_id = Column(String, ForeignKey("issues.id"), nullable=True)
    status = Column(SAEnum(ImplementationStatus), default=ImplementationStatus.QUEUED, nullable=False)
    assigned_to = Column(String(255), nullable=True)
    platform = Column(String(100), nullable=True)
    fix_details = Column(JSON, nullable=True)
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="implementations")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    website_id = Column(String, ForeignKey("websites.id"), nullable=True)
    tier = Column(SAEnum(SubscriptionTier), default=SubscriptionTier.MONTHLY, nullable=False)
    status = Column(SAEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False)
    stripe_subscription_id = Column(String(255), nullable=True)
    price_cents = Column(Integer, nullable=False)
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    auto_renew = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="subscriptions")


class ReportSnapshot(Base):
    __tablename__ = "report_snapshots"

    id = Column(String, primary_key=True, default=generate_uuid)
    audit_id = Column(String, ForeignKey("audits.id"), nullable=False, index=True)
    overall_score = Column(Float, nullable=False)
    category_scores = Column(JSON, nullable=False)  # {"mobile_responsiveness": 85, ...}
    issue_summary = Column(JSON, nullable=False)  # {"total": 12, "critical": 1, ...}
    top_issues = Column(JSON, nullable=True)  # Top 5 issues
    quick_wins = Column(JSON, nullable=True)  # Top 3 quick win fixes
    summary_text = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)

    # Relationships
    audit = relationship("Audit", back_populates="report_snapshots")


class PlatformToken(Base):
    __tablename__ = "platform_tokens"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    website_id = Column(String, ForeignKey("websites.id"), nullable=False, index=True)
    platform = Column(String(100), nullable=False)
    token_type = Column(String(50), nullable=False)  # "api_key", "access_token", "credentials"
    encrypted_token = Column(Text, nullable=False)
    extra_data = Column(JSON, nullable=True)  # e.g., {"site_id": "123", "username": "admin"}
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    website = relationship("Website", back_populates="platform_tokens")

    Index("idx_platform_tokens_website", "website_id")