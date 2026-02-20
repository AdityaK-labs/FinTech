# Production Architecture Blueprint

## Layers

1. **Data Layer**
   - PostgreSQL stores master data, parsed documents, transactions, and audit logs.
   - Extensible hooks for S3/object storage and vector stores for document embeddings.

2. **Reasoning Layer**
   - Transaction classification engine tags entries for GST/TDS applicability.
   - GST reasoning covers output tax, ITC checks, vendor GSTIN validation, and mismatch flags.
   - TDS reasoning evaluates 194C, 194J, 194H, and GST TDS section 51 obligations.
   - Hybrid risk engine blends deterministic penalties with anomaly-style risk amplification.

3. **Reporting Layer**
   - Downloadable report APIs for P&L, Balance Sheet, tax summaries, and explainable logs.
   - Filing abstraction simulates statutory submissions (26Q, GSTR-7).

## Security and IAM

- JWT authentication with role-aware access model.
- Roles: Proprietor, MSME, CA Firm.
- Audit logs persist legal references for each compliance decision.

## Scale and Ops

- Containerized services for independent scaling by workload type.
- API gateway isolates identity + orchestration concerns.
- Services are deployable on Kubernetes/ECS with horizontal autoscaling.
