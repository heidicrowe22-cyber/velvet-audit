-- ===========================================================================
-- Velvet Hour Audit — Portable Database Schema (SQLite / DDL)
-- ===========================================================================
-- This schema matches the SQLAlchemy models in backend/app/models/models.py
-- Use with: sqlite3 velvethour.db < schema.sql
-- ===========================================================================

-- ─── Enums (implemented as TEXT CHECK constraints) ─────────────────────────

-- ─── Users ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    name            TEXT,
    company         TEXT,
    role            TEXT NOT NULL DEFAULT 'customer' CHECK(role IN ('customer','admin','agency')),
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    stripe_customer_id TEXT
);
CREATE INDEX idx_users_email ON users(email);

-- ─── Websites ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS websites (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT NOT NULL REFERENCES users(id),
    url             TEXT NOT NULL,
    domain          TEXT NOT NULL,
    platform        TEXT CHECK(platform IN ('wordpress','shopify','wix','squarespace','webflow','godaddy','custom')),
    name            TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_websites_user_id ON websites(user_id);
CREATE INDEX idx_websites_domain ON websites(domain);

-- ─── Audits ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audits (
    id                  TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    website_id          TEXT NOT NULL REFERENCES websites(id),
    user_id             TEXT NOT NULL REFERENCES users(id),
    status              TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','running','complete','failed')),
    overall_score       REAL,
    page_count_scanned  INTEGER NOT NULL DEFAULT 0,
    error_message       TEXT,
    started_at          TEXT,
    completed_at        TEXT,
    created_at          TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    scan_metadata       TEXT  -- JSON string
);
CREATE INDEX idx_audits_website_id ON audits(website_id);
CREATE INDEX idx_audits_user_id ON audits(user_id);

-- ─── Audit Categories ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_categories (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    audit_id        TEXT NOT NULL REFERENCES audits(id),
    category_name   TEXT NOT NULL,
    display_name    TEXT NOT NULL,
    score           REAL,
    issue_count     INTEGER NOT NULL DEFAULT 0,
    critical_count  INTEGER NOT NULL DEFAULT 0,
    high_count      INTEGER NOT NULL DEFAULT 0,
    medium_count    INTEGER NOT NULL DEFAULT 0,
    low_count       INTEGER NOT NULL DEFAULT 0,
    summary         TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_audit_categories_audit ON audit_categories(audit_id);

-- ─── Issues ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS issues (
    id                  TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    audit_id            TEXT NOT NULL REFERENCES audits(id),
    category_name       TEXT NOT NULL,
    title               TEXT NOT NULL,
    description         TEXT,
    severity            TEXT NOT NULL CHECK(severity IN ('critical','high','medium','low','info')),
    difficulty          TEXT CHECK(difficulty IN ('easy','medium','hard')),
    business_impact     TEXT,
    revenue_impact_pct  REAL,
    affected_element    TEXT,
    recommendation      TEXT,
    fix_preview         TEXT,
    fix_price_cents     INTEGER,
    fix_package_id      TEXT REFERENCES fix_packages(id),
    is_quick_fix        INTEGER NOT NULL DEFAULT 0,
    created_at          TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_issues_audit ON issues(audit_id);
CREATE INDEX idx_issues_category ON issues(audit_id, category_name);

-- ─── Fix Packages ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fix_packages (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name            TEXT NOT NULL,
    description     TEXT,
    price_cents     INTEGER NOT NULL,
    estimated_hours REAL,
    estimated_days  INTEGER,
    is_bundle       INTEGER NOT NULL DEFAULT 0,
    max_issues      INTEGER,
    categories      TEXT,  -- JSON list of category names
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- Default fix packages
INSERT OR IGNORE INTO fix_packages (id, name, description, price_cents, estimated_days, is_bundle) VALUES
    ('quick_fix',     'Quick Fix',     'Simple text/code change for a single issue',               2900,  1, 0),
    ('standard_fix',  'Standard Fix',  'Moderate complexity fix for one category',                7900,  2, 0),
    ('category_fix',  'Category Fix',  'Full optimization of one audit category',                 14900, 3, 0),
    ('bundle_fix',    'Bundle Fix',    '3-5 related fixes across multiple categories',             29900, 5, 1);

-- ─── Orders ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    id                      TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id                 TEXT NOT NULL REFERENCES users(id),
    audit_id                TEXT REFERENCES audits(id),
    status                  TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','paid','processing','completed','refunded','cancelled')),
    total_cents             INTEGER NOT NULL,
    stripe_payment_intent_id TEXT,
    stripe_session_id       TEXT,
    notes                   TEXT,
    created_at              TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at              TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    paid_at                 TEXT
);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_audit_id ON orders(audit_id);

-- ─── Order Items ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS order_items (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_id        TEXT NOT NULL REFERENCES orders(id),
    fix_package_id  TEXT REFERENCES fix_packages(id),
    issue_id        TEXT REFERENCES issues(id),
    description     TEXT NOT NULL,
    price_cents     INTEGER NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- ─── Implementations ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS implementations (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    order_id        TEXT NOT NULL REFERENCES orders(id),
    audit_id        TEXT REFERENCES audits(id),
    issue_id        TEXT REFERENCES issues(id),
    status          TEXT NOT NULL DEFAULT 'queued' CHECK(status IN ('queued','in_progress','qa_review','completed','failed')),
    assigned_to     TEXT,
    platform        TEXT,
    fix_details     TEXT,  -- JSON
    deployed_at     TEXT,
    completed_at    TEXT,
    notes           TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_implementations_order ON implementations(order_id);

-- ─── Subscriptions ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS subscriptions (
    id                      TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id                 TEXT NOT NULL REFERENCES users(id),
    website_id              TEXT REFERENCES websites(id),
    tier                    TEXT NOT NULL DEFAULT 'monthly' CHECK(tier IN ('monthly','annual')),
    status                  TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','paused','cancelled','expired')),
    stripe_subscription_id  TEXT,
    price_cents             INTEGER NOT NULL,
    current_period_start    TEXT,
    current_period_end      TEXT,
    auto_renew              INTEGER NOT NULL DEFAULT 1,
    created_at              TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at              TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    cancelled_at            TEXT
);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);

-- ─── Report Snapshots ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS report_snapshots (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    audit_id        TEXT NOT NULL REFERENCES audits(id),
    overall_score   REAL NOT NULL,
    category_scores TEXT NOT NULL,  -- JSON: {"mobile_responsiveness": 85, ...}
    issue_summary   TEXT NOT NULL,  -- JSON: {"total": 12, "critical": 1, ...}
    top_issues      TEXT,           -- JSON array
    quick_wins      TEXT,           -- JSON array
    summary_text    TEXT,
    generated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    is_published    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_report_snapshots_audit ON report_snapshots(audit_id);

-- ─── Platform Tokens ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS platform_tokens (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT NOT NULL REFERENCES users(id),
    website_id      TEXT NOT NULL REFERENCES websites(id),
    platform        TEXT NOT NULL,
    token_type      TEXT NOT NULL,
    encrypted_token TEXT NOT NULL,
    metadata        TEXT,  -- JSON
    is_active       INTEGER NOT NULL DEFAULT 1,
    expires_at      TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_platform_tokens_website ON platform_tokens(website_id);

-- ===========================================================================
-- Seed Data: Fix Packages (already inserted above)
-- ===========================================================================

-- Create an admin user if none exists (password: admin123)
-- Hash: $2b$12$... (bcrypt hash of "admin123")
-- To generate: python3 -c 'import bcrypt; print(bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode())'
INSERT OR IGNORE INTO users (id, email, password_hash, name, role, is_active)
VALUES ('admin-001', 'admin@velvethour.com',
        '$2b$12$LJ3m4ys3Lk0TSwHCpNqrOeOEKYz7lATEGr/CwONb5RrQJPmFrw1aK',
        'Admin', 'admin', 1);

-- ===========================================================================
-- NOTE: This is a reference schema. In production, use the Python
-- SQLAlchemy ORM via `scripts/setup_db.py` which handles migrations.
-- ===========================================================================