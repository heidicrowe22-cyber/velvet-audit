# Velvet Hour Audit — Product Requirements Document (PRD)

> **Version:** 1.0  
> **Author:** Architect & Backend Engineer  
> **Status:** Draft  

---

## 1. Executive Summary

Velvet Hour Audit is an AI-powered website auditing platform that scans any small business website, identifies issues across 17 categories, scores them, and provides actionable fixes — from quick wins to full implementations. The platform doesn't just find problems; it estimates business impact, provides clear pricing for fixes, and executes them for a flat fee.

### Core Value Proposition
Small business owners get agency-level insights without hiring an agency.

---

## 2. Target Audience

| Persona | Pain Points | Needs |
|---------|-------------|-------|
| **Small business owner** (realtor, salon, roofer, restaurant, boutique, etc.) | Knows website matters but lacks time, expertise, or budget for a dedicated web team | Simple audit, clear recommendations, done-for-you fixes |
| **Local agency / freelancer** | Needs to deliver audits to clients efficiently, wants white-label capability | White-label reports, bulk auditing, API access |

---

## 3. User Flows

### Flow 1: Free Audit (Conversion Funnel)
```
Homepage → Enter Website URL → [Scanning Animation] → Report Generated → View Scores → Browse Issues → See Fix Options → Payment → Fixes Implemented
```

1. **Landing**: User arrives at VelvetHour.com
2. **URL Input**: Enters their website URL
3. **Scanning**: Platform scans the website (~30-60 seconds for full audit)
4. **Free Report**: User sees a comprehensive report with:
   - Overall score (0-100)
   - Per-category scores with severity indicators
   - Issue count per category
   - Top 3 quick wins (free)
   - Business impact estimates (e.g., "This issue may cost you 12% of conversions")
5. **Fix Selection**: User can browse all issues, see fix pricing
6. **Payment**: User selects fixes → payment via Stripe
7. **Implementation**: Platform implements fixes within 5 business days
8. **Re-audit**: User gets updated scores showing improvement

### Flow 2: Subscription (Upsell)
- Monthly monitoring
- Periodic re-audits
- Automated minor fixes
- Priority implementation

### Flow 3: White-Label (Agency)
- Custom branding on reports
- Bulk audit management
- API access

---

## 4. The 17 Audit Categories

Each category has:
- **Score** (0-100)
- **Issues** (individual problems found)
- **Severity** (Critical, High, Medium, Low, Info)
- **Business impact estimate** (conversion/revenue loss)
- **Implementation difficulty** (Easy, Medium, Hard)
- **Fix pricing** (free, $29, $79, $149, $299, custom quote)

### Category Definitions

| # | Category | Key Checks | Typical Issues |
|---|----------|-----------|----------------|
| 1 | **Mobile Responsiveness** | Viewport meta tag, responsive media queries, touch target sizes, font scaling, horizontal scroll | Non-responsive layout, tiny tap targets, broken mobile nav |
| 2 | **Page Speed** | LCP, FID, CLS, TTFB, render-blocking resources, image compression, caching | Slow LCP (>2.5s), high CLS, unoptimized images |
| 3 | **SEO Fundamentals** | Meta titles/descriptions, heading hierarchy, canonical tags, sitemap, robots.txt, schema markup | Missing meta descriptions, duplicate titles, no schema |
| 4 | **Local SEO** | NAP consistency, Google Business Profile linkage, local citations, geo-targeted content | Inconsistent address/phone, no local schema |
| 5 | **Accessibility** | WCAG 2.1 AA compliance, alt text, color contrast, keyboard navigation, aria labels | Missing alt text, low contrast, non-keyboard-accessible |
| 6 | **User Experience** | Layout clarity, visual hierarchy, whitespace usage, typography, color harmony | Cluttered layout, poor typography, jarring colors |
| 7 | **Navigation** | Menu structure, breadcrumbs, footer links, search functionality, logical flow | Broken nav, confusing menu structure, missing breadcrumbs |
| 8 | **Conversion Optimization** | Form design, button placement, checkout flow, lead capture, landing page coherence | Multi-step forms that could be simpler, weak CTAs |
| 9 | **Calls to Action** | CTA visibility, copy effectiveness, placement, urgency, button styling | Weak "Submit" instead of "Get My Free Quote", buried CTAs |
| 10 | **Contact Visibility** | Phone, email, contact form, physical address, click-to-call on mobile | Missing contact info above fold, no click-to-call |
| 11 | **Trust Signals** | SSL, privacy policy, terms of service, about page, testimonials, trust badges | Missing privacy policy, no testimonials, no about page |
| 12 | **Reviews & Reputation** | Review widget integration, review schema, social proof, rating display | No review schema, not displaying testimonials |
| 13 | **Content Quality** | Grammar, readability, value proposition clarity, blog freshness, duplicate content | Thin content, outdated blog, poor value prop |
| 14 | **Image Optimization** | Compression, alt tags, proper formats (WebP), lazy loading, responsive images | Large unoptimized images, missing alt text, no lazy loading |
| 15 | **Security Basics** | HTTPS, SSL validity, form security, safe external links, no mixed content | HTTP pages, expired SSL, mixed content warnings |
| 16 | **Technical Issues** | Broken links, 404s, redirect chains, console errors, JS errors, rendering issues | 404 pages, redirect chains, JS console errors |
| 17 | **Lead Generation** | Form placement, newsletter signup, booking/scheduling integration, lead magnets | No lead capture form, no newsletter signup, no booking integration |

---

## 5. Scoring System

### Overall Score = Weighted average of 17 category scores

| Category | Weight |
|----------|--------|
| Mobile Responsiveness | 9% |
| Page Speed | 9% |
| SEO Fundamentals | 8% |
| Local SEO | 7% |
| Accessibility | 7% |
| User Experience | 7% |
| Navigation | 6% |
| Conversion Optimization | 8% |
| Calls to Action | 7% |
| Contact Visibility | 6% |
| Trust Signals | 6% |
| Reviews & Reputation | 4% |
| Content Quality | 5% |
| Image Optimization | 4% |
| Security Basics | 3% |
| Technical Issues | 2% |
| Lead Generation | 2% |

### Severity Levels & Scoring Impact

| Severity | Points Deducted | Business Impact Tag |
|----------|----------------|---------------------|
| Critical | -30 | "Urgent — fix now" |
| High | -15 | "Important — impacts revenue" |
| Medium | -7 | "Should fix" |
| Low | -3 | "Nice to have" |
| Info | 0 | "FYI" |

---

## 6. Fix System Design

### Fix Types

| Type | Description | Price | Timeline |
|------|-------------|-------|----------|
| **Quick Fix** | Simple code/text change, single issue | $29 | <24 hours |
| **Standard Fix** | Moderate complexity, single category fix | $79 | 1-2 days |
| **Category Fix** | Full optimization of one category | $149 | 2-3 days |
| **Bundle Fix** | 3-5 related fixes across categories | $299 | 3-5 days |
| **Full Site Overhaul** | Comprehensive fix of all critical issues | Custom quote | 1-2 weeks |

### Implementation Pipeline
```
Fix Selected → Payment → Task Assigned to Implementation Team → Work Done → QA Review → Deploy → Re-audit → Customer Notified
```

---

## 7. Platform Integrations

| Platform | Fix Method | Authentication |
|----------|-----------|---------------|
| **WordPress** | Plugin/API + direct DB | WP Admin credentials or API key |
| **Shopify** | Theme editor + Shopify API | Shopify API token |
| **Wix** | Wix Editor API | Wix API key |
| **Squarespace** | Squarespace API | API key |
| **Webflow** | Designer API + custom code injection | Webflow API token |
| **GoDaddy Website Builder** | Manual (limited API) | Admin credentials |
| **Custom HTML/CSS/JS** | Direct code injection via FTP/SFTP/CLI | Server access or Git deploy |

### Integration Strategy (Phase 1)
Start with **WordPress** and **Custom HTML** — these cover the majority of small business websites. Add Shopify, Wix, Squarespace, and Webflow in Phase 2. GoDaddy and other proprietary builders in Phase 3.

---

## 8. Dashboard Features

### Customer Dashboard
- Audit history (list of past audits with scores)
- Current audit report (detailed view)
- Fix recommendations (browse, select, purchase)
- Implementation status (tracking)
- Re-audit results (before/after comparison)
- Subscription management
- Billing history

### Admin Dashboard
- All customers (list, search, filter)
- All audits (pending, running, complete)
- Implementation queue
- Revenue dashboard
- Platform analytics
- White-label management
- System health

---

## 9. Pricing Strategy

| Tier | Price | What's Included |
|------|-------|-----------------|
| **Free Audit** | $0 | Full audit report with scores, issue descriptions, business impact, top 3 quick fixes identified |
| **Quick Fix** | $29/ea | Single simple fix (e.g., meta description, alt text) |
| **Standard Fix** | $79/category | Full fix of one category's issues |
| **Bundle** | $299 | Up to 5 related fixes |
| **Monthly Monitoring** | $49/mo | Monthly re-audit, score tracking, automated minor fixes, priority pricing on new fixes |
| **White-Label** | Custom | Agency branding, bulk audits, API access |

---

## 10. Technical Architecture

### Stack Decision

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Backend** | Python FastAPI | Async support for concurrent scanning, strong AI/ML ecosystem, excellent typing |
| **Frontend** | React + Vite | Fast builds, excellent DX, component reusability |
| **Database** | SQLite via Turso/team-db | Serverless, synced, simple schema management |
| **Crawler/Scanner** | Playwright (Python) | Modern browser automation, async-native, better than Puppeteer for Python |
| **Queue** | Redis / RQ | Lightweight task queue for async audit jobs |
| **Payment** | Stripe | Industry standard, webhook support, simple API |
| **Auth** | Supabase or JWT-based | Simple authentication for MVP |
| **Deployment** | Docker + VPS or Railway | Simple, cost-effective for MVP |

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Landing  │  │ Audit    │  │ Dashboard│  │ Admin      │  │
│  │ Page     │  │ Report   │  │          │  │ Panel      │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────────┐
│                    Backend (FastAPI)                          │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Auth     │  │ Audit API  │  │ Fix API  │  │ Payment   │  │
│  │ Module   │  │            │  │          │  │ Webhooks  │  │
│  └──────────┘  └────────────┘  └──────────┘  └───────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Scanning Engine (Playwright)                 │
│  ┌──────────┐  ┌────────────┐  ┌────────────┐  ┌─────────┐  │
│  │ Crawler  │  │ Category   │  │ AI         │  │ Rules   │  │
│  │ Engine   │  │ Scanners   │  │ Enhancer   │  │ Engine  │  │
│  └──────────┘  └────────────┘  └────────────┘  └─────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     Data Layer                                │
│  ┌──────────┐  ┌────────────┐  ┌────────────┐  ┌─────────┐  │
│  │ SQLite   │  │ Redis      │  │ File Store │  │ Stripe  │  │
│  │ (Turso)  │  │ (Queue)    │  │ (Assets)   │  │         │  │
│  └──────────┘  └────────────┘  └────────────┘  └─────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Scanning Strategy: Hybrid Rules + AI

**Phase 1 (MVP): 100% Rules-Based**
- Faster, deterministic, cheaper
- All 17 categories have defined checks
- Uses regex, DOM queries, HTTP headers analysis, Lighthouse-like metrics

**Phase 2: AI-Enhanced**
- Use LLM to analyze content quality, CTA effectiveness, UX
- Generate natural language fix descriptions
- Estimate business impact more accurately

---

## 11. Database Schema (Conceptual)

### Core Tables
- `users` — user accounts (customers and admins)
- `websites` — websites being audited
- `audits` — individual audit sessions
- `audit_categories` — per-category scores for each audit
- `issues` — individual issues found during audit
- `fixes` — available fix packages
- `orders` — customer purchases
- `order_items` — individual fix items in an order
- `implementations` — fix implementation tracking
- `subscriptions` — monthly subscription records
- `reports` — generated report snapshots
- `platform_tokens` — stored credentials for platform integrations

(Full schema defined in implementation phase)

---

## 12. API Endpoints (v1)

### Public
- `POST /api/v1/audits` — Start a new audit
- `GET /api/v1/audits/{id}` — Get audit results
- `GET /api/v1/audits/{id}/issues` — Get all issues for an audit
- `GET /api/v1/audits/{id}/report` — Get formatted report
- `POST /api/v1/fixes/estimate` — Get pricing for fixing specific issues

### Authenticated (Customer)
- `GET /api/v1/customer/audits` — List user's audits
- `POST /api/v1/orders` — Create order (purchase fixes)
- `GET /api/v1/orders/{id}` — Get order status
- `GET /api/v1/subscription` — Get subscription details
- `POST /api/v1/customer/tokens` — Store platform credentials

### Admin
- `GET /api/v1/admin/customers` — List all customers
- `GET /api/v1/admin/audits` — List all audits
- `GET /api/v1/admin/implementations` — Implementation queue
- `PATCH /api/v1/admin/implementations/{id}` — Update implementation status

### Webhooks
- `POST /api/v1/webhooks/stripe` — Stripe payment events

---

## 13. Future Expansion Plan

### Phase 1 (MVP) — 4-6 weeks
- [x] Core scanning engine (rules-based, all 17 categories)
- [x] Free audit report generation
- [x] Fix recommendation with pricing
- [x] Payment processing (Stripe)
- [x] Fix implementation workflow
- [x] User dashboard (basic)
- [ ] WordPress integration

### Phase 2 — 8-12 weeks
- [ ] AI-enhanced content analysis
- [ ] AI-generated fix descriptions
- [ ] Shopify, Wix integrations
- [ ] Monthly subscription (monitoring)
- [ ] Admin dashboard
- [ ] Re-audit & score tracking

### Phase 3 — 12-16 weeks
- [ ] White-label agency portal
- [ ] Bulk audit management
- [ ] Real-time monitoring
- [ ] Advanced analytics
- [ ] API for third-party integration
- [ ] Auto-fix (automatic deployment of minor fixes)

---

## 14. Success Metrics (KPIs)

| KPI | Target |
|-----|--------|
| Audit completion rate | >80% (users who start → get report) |
| Free audit → paid fix conversion | >10% |
| Average revenue per paid customer | $150+ |
| Fix delivery time | <5 business days |
| Customer satisfaction (post-fix) | >4.5/5 |
| Repeat purchase rate | >25% |
| Month-over-month revenue growth | >20% |

---

## 15. Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Scanning breaks on complex SPAs | Medium | Multiple fallback strategies, timeout handling |
| AI-generated estimates inaccurate | Medium | Start rules-based, validate AI before launch |
| Fix implementation scope creep | High | Clear scope definition in each fix package, change order process |
| Platform API changes (WordPress etc.) | Medium | Abstract integration layer, monitor API changes |
| Competitive pressure (PageSpeed, SEMrush) | Low | Focus on SMB niche, done-for-you execution differentiates |