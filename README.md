# Autonomous Compliance Intelligence Platform

Production-grade monorepo for an AI-powered compliance SaaS targeting Indian GST, TDS, and Income Tax auditing.

## Architecture

- **Frontend**: Next.js 14 + TypeScript dashboard (`apps/web`)
- **Backend**: FastAPI microservices (`services/*`)
  - `gateway`: JWT auth, onboarding, orchestration, reporting
  - `ingestion`: document intake + OCR/parser abstraction
  - `compliance`: GST/TDS/Income tax reasoning endpoints
  - `anomaly`: hybrid rule + ML-style anomaly scoring
- **Data**: PostgreSQL for users, documents, transactions, audit logs
- **Deployment**: Docker Compose for local production-like stack

## Key capabilities

- Role-based onboarding (`PROPRIETOR`, `MSME`, `CA_FIRM`)
- JWT-secured APIs
- Document ingestion pipeline for bank statements, GST returns, invoices, ITRs
- Transaction classification engine
- GST engine with Section 17(5), GSTIN validation, and 2A-style matching
- Unified TDS engine: 194C, 194J, 194H + GST TDS Section 51
- Hybrid risk score engine using rule + anomaly blend
- Explainable audit logs with tax section references
- Downloadable P&L, Balance Sheet, and Tax Summary JSON reports
- Filing simulation APIs (26Q / GSTR-7)

## Quick start

```bash
docker compose up --build
```

Frontend: `http://localhost:3000`
Gateway API docs: `http://localhost:8000/docs`
