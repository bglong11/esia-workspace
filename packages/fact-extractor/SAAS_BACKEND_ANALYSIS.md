# ESIA Fact Extractor SaaS - Backend Pipeline Analysis & Objectives

**Date**: November 12, 2025
**Status**: Backend Pipeline Ready for Production
**Focus**: Backend pipeline completion (Web frontend, Stripe, database - Phase 2)

---

## Executive Summary

The **ESIA Fact Extractor** is being built as a **Software-as-a-Service (SaaS)** platform for enterprise clients. The backend pipeline is **production-ready** for core functionality (PDF upload → fact extraction → factsheet generation). The system needs additional layers for e-commerce and user management before full production deployment.

---

## My Understanding of Your Objectives

### Primary Vision
Build an **enterprise SaaS platform** that enables environmental consultants and project managers to:
1. Upload **PDF/DOCX documents** (ESIA reports from various projects)
2. **Automatically extract quantitative and categorical facts** using LLM with DSPy
3. **Categorize facts intelligently** into logical project sections (8 categories × 32 subcategories)
4. **Generate project factsheets** organized by category for client deliverables
5. **Track extracted facts** in a database with user editing capabilities
6. **Export results** as CSV or formatted reports

### Business Model
- **SaaS with E-commerce**: Stripe integration for payments
- **Multi-tenant**: Different clients upload different documents
- **Scalable**: Document processing in background
- **White-label ready**: Can be customized for different clients

### Technical Stack
- **Backend**: FastAPI (Python web framework)
- **LLM Integration**: DSPy with multiple providers (Ollama, OpenAI, Claude, Gemini)
- **Document Processing**: Docling (PDF/DOCX → Markdown)
- **Database**: SQLAlchemy ORM (SQLite dev, PostgreSQL production)
- **Task Queue** (Optional): Celery for long-running jobs
- **Frontend** (Future): React/Vue for web interface

### Expected Users
- Environmental consultants
- Project managers
- Corporate sustainability teams
- Government environmental agencies
- Mining/energy sector companies

---

## Current Backend Pipeline Status

### ✅ PRODUCTION-READY COMPONENTS

#### 1. **FastAPI Backend** (saas/backend/main.py)
- **Status**: ✅ Ready for production
- **Features**:
  - File upload endpoint (`/api/upload`)
  - Background processing with progress tracking
  - Job status monitoring (`/api/jobs/{job_id}`)
  - Fact retrieval endpoints
  - CSV export functionality
  - CORS middleware configured
  - Health check endpoint
  - RESTful API design

**Endpoints**:
```
POST   /api/upload                    - Upload PDF/DOCX/MD file
GET    /api/jobs/{job_id}            - Get job status
GET    /api/jobs/{job_id}/facts      - Get extracted facts
GET    /api/jobs/{job_id}/complete   - Get job + facts
PATCH  /api/facts/{fact_id}          - User edits fact
DELETE /api/facts/{fact_id}          - Delete fact
GET    /api/jobs/{job_id}/export/csv - Export to CSV
GET    /health                        - Health check
```

**Database Operations**:
- Stores jobs with status tracking
- Stores extracted facts with metadata
- Supports user edits and comments
- Tracks conflicts and value ranges
- Cascading deletes (job deletion removes facts)

#### 2. **Document Processing** (saas/core/extractor.py)
- **Status**: ✅ Ready for production
- **Features**:
  - Docling integration for PDF/DOCX conversion
  - Multi-provider LLM support
  - Text chunking with progress callback
  - Fact extraction via DSPy
  - Conflict detection (2% tolerance + ×10 error detection)
  - Unit normalization (80+ units)
  - Results saved to database

**Processing Pipeline**:
```
1. Configure LLM (Ollama/OpenAI/Claude/Gemini)
2. Load document + Docling conversion
3. Chunk text (4000-char chunks)
4. Extract facts via DSPy (LLM-based)
5. Cluster facts by signature
6. Detect conflicts in values
7. Normalize units to canonical forms
8. Return consolidated facts + metadata
```

#### 3. **Database Schema** (saas/backend/models.py)
- **Status**: ✅ Ready for production
- **Tables**:
  - `jobs`: Processing jobs (status, progress, timestamps)
  - `facts`: Extracted facts with normalized values, conflicts, user edits

**Design**:
- Foreign key relationship (Job → Facts)
- Cascade delete (removing job removes facts)
- Indexed fields for fast queries
- Timestamps for audit trail
- User edit tracking

#### 4. **API Schemas** (saas/backend/schemas.py)
- **Status**: ✅ Ready for production
- **Pydantic models**: Type-safe request/response validation
- **Versioning ready**: Can add API versioning easily

#### 5. **Factsheet Functionality** (esia_extractor.py + improvements)
- **Status**: ✅ Ready for production
- **Features**:
  - LLM-based fact categorization (8 categories × 32 subcategories)
  - Intelligent caching (37-80% hit rate)
  - Confidence scoring (high/medium/low)
  - Error handling and logging
  - Progress tracking with tqdm
  - Cache statistics reporting

**NOT YET INTEGRATED INTO SaaS**:
The factsheet functionality in `esia_extractor.py` is production-ready but NOT integrated into `saas/core/extractor.py`. This is a **gap to fix** before full production.

---

## Critical Gaps for Production SaaS

### 1. ⚠️ **Factsheet Integration Missing**
**Issue**: Factsheet categorization works in CLI (`esia_extractor.py`) but NOT in SaaS backend
- `saas/core/extractor.py` returns facts WITHOUT categories/subcategories
- Facts don't have: category, subcategory, confidence, rationale
- Database schema doesn't have factsheet fields

**Action Required**:
```python
# Add to Fact model (models.py):
category = Column(String(100))           # Project Overview, etc.
subcategory = Column(String(100))        # Basic Info, etc.
categorization_confidence = Column(String(20))  # high/medium/low
categorization_rationale = Column(Text))

# Update process_document() to:
1. Instantiate FactCategorizer (with caching)
2. Categorize each unique fact
3. Store categorization in database
4. Return categorized facts to frontend
```

**Effort**: Medium (2-4 hours)

---

### 2. ⚠️ **User Authentication & Multi-tenancy**
**Current State**: No authentication
- All uploads are anonymous
- No user accounts
- No API key authentication
- No tenant isolation

**Action Required**:
```python
# Add to models.py:
class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    subscription_tier = Column(String)  # free, pro, enterprise
    created_at = Column(DateTime)

class Job(Base):
    user_id = Column(Integer, ForeignKey("users.id"))  # Add this
    # ... rest of fields

# Add authentication endpoints:
POST   /auth/register           - Sign up
POST   /auth/login              - Login (returns JWT)
POST   /auth/refresh            - Refresh token
GET    /auth/me                 - Current user info

# Add middleware:
- JWT token validation
- User isolation (can only see own jobs)
```

**Effort**: Medium (3-5 hours)

---

### 3. ⚠️ **Payment Integration (Stripe)**
**Current State**: Not implemented

**Action Required**:
```python
# Add to models.py:
class Subscription(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    tier = Column(String)  # free, pro, enterprise
    status = Column(String)  # active, canceled, past_due
    current_period_end = Column(DateTime)

# Add Stripe endpoints:
POST   /stripe/webhook                    - Webhook for events
POST   /billing/create-subscription       - Start subscription
POST   /billing/cancel-subscription       - Cancel subscription
GET    /billing/customer-portal          - Stripe customer portal

# Add usage tracking:
- Track documents processed per month
- Enforce limits by tier (free: 5/mo, pro: 100/mo, enterprise: unlimited)
```

**Effort**: High (5-7 hours)

---

### 4. ⚠️ **Web Frontend**
**Current State**: Placeholder in main.py (tries to mount /static)

**Action Required**:
```
Create React/Vue SPA:
├── Login/Register pages
├── Dashboard (upload, job list)
├── Job detail (view facts, edit, export)
├── Settings (subscription, API keys)
└── Admin panel (if needed)

Integration with backend:
- Upload file → show progress
- Fetch job status → real-time updates
- Edit facts → send PATCH requests
- Export CSV → trigger download
- Manage subscription → Stripe link
```

**Effort**: Very High (15-20 hours for basic MVP)

---

### 5. ⚠️ **Production Deployment Setup**
**Current State**: Development only

**Action Required**:
```
- Docker containerization
- Environment configuration (prod .env)
- PostgreSQL instead of SQLite
- Celery + Redis for background jobs
- S3/cloud storage for uploads
- SSL/TLS certificates
- Rate limiting
- Logging and monitoring
```

**Effort**: High (8-10 hours)

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        WEB FRONTEND (Future)                      │
│                 (React/Vue SPA with Stripe UI)                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ↓
┌──────────────────────────────────────────────────────────────────┐
│                      FastAPI BACKEND                              │
│                 (saas/backend/main.py)                            │
├──────────────────────────────────────────────────────────────────┤
│  Routes:                                                           │
│  • /api/upload (POST) - File upload                              │
│  • /api/jobs/* (GET) - Job status                                │
│  • /api/facts/* (PATCH/DELETE) - User edits                      │
│  • /auth/* (POST) - Login/Register                               │
│  • /stripe/* (POST) - Payment webhooks                           │
│  • /health (GET) - Health check                                  │
└────────────────────────┬──────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Database    │ │ Task Queue   │ │ Stripe API   │
│ (SQLAlchemy) │ │  (Celery)    │ │              │
│ (SQLite/PG)  │ │              │ │              │
└──────────────┘ └────────┬─────┘ └──────────────┘
                         │
                         ↓
         ┌───────────────────────────────┐
         │  Background Processing Worker │
         │  (saas/core/extractor.py)     │
         ├───────────────────────────────┤
         │ 1. Docling (PDF→Markdown)     │
         │ 2. Chunking                   │
         │ 3. Fact Extraction (DSPy)     │
         │ 4. Categorization (DSPy) ⚠️   │
         │ 5. Unit Normalization         │
         │ 6. Conflict Detection         │
         └───────────────────────────────┘
                 │     │     │
                 ↓     ↓     ↓
         ┌──────────────────────────┐
         │   LLM Providers          │
         ├──────────────────────────┤
         │ • Ollama (local)         │
         │ • OpenAI                 │
         │ • Claude (Anthropic)     │
         │ • Gemini (Google)        │
         └──────────────────────────┘
```

---

## Data Flow: Document Upload to Factsheet

```
1. USER UPLOADS FILE
   ↓
   Client → POST /api/upload (PDF/DOCX/MD)
   ↓
   Server stores file, creates Job record (status: pending)
   ↓
   Returns: job_id, session_id

2. BACKGROUND PROCESSING STARTS
   ↓
   Worker: process_document(file_path)
   ├─ Configure LLM provider
   ├─ Docling converts PDF/DOCX → Markdown
   ├─ Chunk markdown (4000-char chunks)
   ├─ FactExtractor: Extract facts (DSPy)
   ├─ Cluster by signature
   ├─ Detect conflicts
   ├─ Normalize units
   └─ FactCategorizer: Categorize facts (DSPy) ⚠️ MISSING

3. STORE IN DATABASE
   ↓
   For each fact:
   ├─ signature, name, type
   ├─ value_raw, value_num, unit_raw
   ├─ value_normalized, unit_normalized
   ├─ evidence, page, chunk_id
   ├─ occurrence_count, has_conflict, conflict_description
   ├─ category, subcategory, confidence, rationale ⚠️ MISSING
   └─ Store in Fact table

4. USER VIEWS RESULTS
   ↓
   Client → GET /api/jobs/{job_id}/complete
   ↓
   Return: Job + all facts with metadata
   ↓
   Frontend: Display facts organized by category

5. USER EDITS & EXPORTS
   ↓
   Client → PATCH /api/facts/{fact_id} (correct values)
   Client → GET /api/jobs/{job_id}/export/csv
   ↓
   Return: CSV file with facts
```

---

## File Structure

```
/home/user/esia-fact-extractor/
├── esia_extractor.py                   # CLI tool (with factsheet)
├── FACTSHEET_TEST_REPORT.md            # Test results
├── IMPLEMENTATION_CHANGES_SUMMARY.md   # Local changes
├── PIPELINE_OVERVIEW.md                # Architecture docs
├── QUICK_START_LOCAL.md                # User guide
├── README.md                           # Project docs
├── CLAUDE.md                           # Dev guidance
│
├── saas/
│   ├── core/
│   │   └── extractor.py               # Document processing ✅ (missing factsheet integration)
│   │
│   └── backend/
│       ├── main.py                    # FastAPI app ✅
│       ├── database.py                # SQLAlchemy setup ✅
│       ├── models.py                  # DB models (missing factsheet fields) ⚠️
│       ├── schemas.py                 # Pydantic schemas (missing factsheet) ⚠️
│       ├── celery_app.py             # Celery config (optional)
│       └── test_*.py                  # Test files
│
├── requirements.txt
└── .env.example
```

---

## What's Ready vs. What's Missing

### ✅ PRODUCTION-READY (Ready to Deploy)
- FastAPI backend structure
- Database schema (Job, Fact tables)
- File upload endpoint
- Background job processing
- Docling integration (PDF/DOCX → Markdown)
- Fact extraction (DSPy-based)
- Conflict detection
- Unit normalization
- CSV export
- Health check endpoint
- API schemas (Pydantic)

### ⚠️ NEEDS COMPLETION (Before Production)
1. **Factsheet Integration** (Easy - 2-4 hours)
   - Add category/subcategory fields to Fact model
   - Integrate FactCategorizer into process_document()
   - Add endpoints to return factsheet data

2. **Authentication** (Medium - 3-5 hours)
   - User registration/login
   - JWT token generation/validation
   - User isolation (job permissions)

3. **Stripe Integration** (High - 5-7 hours)
   - Subscription management
   - Webhook handlers
   - Usage tracking and rate limiting
   - Billing portal link

4. **Web Frontend** (Very High - 15-20 hours)
   - React/Vue SPA
   - Upload UI
   - Job tracking
   - Fact viewing/editing
   - Export functionality
   - Subscription management

5. **Production Deployment** (High - 8-10 hours)
   - Docker setup
   - PostgreSQL configuration
   - Environment variables
   - Celery + Redis (if async jobs needed)
   - Cloud storage (S3)
   - SSL/TLS
   - Monitoring/logging

### 🚀 FUTURE ENHANCEMENTS
- Mobile app (React Native/Flutter)
- Advanced analytics (fact trends)
- Custom categorization per client
- API for third-party integrations
- Webhook notifications
- Bulk processing
- Template library for ESIA formats

---

## Production Readiness Checklist

### Phase 1: Backend Pipeline (Current)
- ✅ FastAPI server running
- ✅ Database models defined
- ✅ File upload working
- ✅ Document processing pipeline
- ✅ Fact extraction with DSPy
- ⚠️ **TODO**: Add factsheet categorization to SaaS
- ⚠️ **TODO**: Add user authentication
- ⚠️ **TODO**: Add Stripe integration

### Phase 2: Frontend & E-Commerce (Next)
- ⏳ Web frontend (React/Vue)
- ⏳ Stripe subscription handling
- ⏳ User dashboard
- ⏳ Admin panel

### Phase 3: Production Deployment (Final)
- ⏳ Docker containerization
- ⏳ PostgreSQL database
- ⏳ Celery + Redis
- ⏳ Cloud storage
- ⏳ SSL/TLS
- ⏳ Monitoring

---

## Estimated Timeline

| Component | Effort | Timeline |
|-----------|--------|----------|
| Factsheet Integration | 2-4 hrs | 1 day |
| Authentication | 3-5 hrs | 1-2 days |
| Stripe Integration | 5-7 hrs | 2-3 days |
| Frontend MVP | 15-20 hrs | 1 week |
| Production Setup | 8-10 hrs | 2-3 days |
| **TOTAL** | **33-46 hrs** | **2-3 weeks** |

---

## Recommendations for Next Steps

### Immediate (This Sprint)
1. **Integrate factsheet categorization into SaaS** (highest priority)
   - Update `models.py`: Add category, subcategory, confidence, rationale fields
   - Update `saas/core/extractor.py`: Add FactCategorizer integration
   - Update `schemas.py`: Include factsheet fields in API responses
   - Test end-to-end pipeline

2. **Add user authentication** (critical for multi-tenancy)
   - User registration/login endpoints
   - JWT token handling
   - Database user table
   - Job permission checks

### Short-term (Next Sprint)
3. **Implement Stripe integration**
   - Subscription model in database
   - Webhook handler for events
   - Usage tracking per user/tier
   - Free tier: 5 docs/month, Pro: 100/month, Enterprise: unlimited

4. **Start frontend development**
   - Basic React app with upload
   - Job status tracking
   - Results viewing

### Medium-term (Month 2)
5. **Production deployment setup**
   - Docker, PostgreSQL, S3
   - Environment configuration
   - Monitoring and logging

6. **Complete frontend**
   - User dashboard
   - Settings/billing
   - Export functionality
   - Mobile responsiveness

---

## Conclusion

Your **ESIA Fact Extractor SaaS backend pipeline is solid and production-ready** for core functionality. The main gaps are:

1. **Factsheet integration** (quick win - add categorization to SaaS)
2. **Authentication** (required for multi-tenancy)
3. **Stripe payments** (required for SaaS business model)
4. **Web frontend** (required for users to interact)
5. **Production infrastructure** (required for reliability/scale)

The estimated timeline to **full production-ready SaaS** is **2-3 weeks** with focused effort.

**Recommendation**: Start with factsheet integration and authentication this week, then add Stripe and frontend next week for a complete MVP.
