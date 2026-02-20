from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.engines.classification_engine import classify_transaction
from app.engines.gst_engine import compute_gst
from app.engines.risk_engine import generate_risk_score
from app.engines.tds_engine import compute_tds
from app.models.entities import AuditLog, Document, Transaction, User
from app.models.schemas import (
    DocumentIngestionRequest,
    GSTComputationRequest,
    ReportResponse,
    RiskScoreRequest,
    TDSComputationRequest,
    TransactionInput,
)
from app.routers.deps import get_current_user

router = APIRouter(prefix='/compliance', tags=['compliance'])


@router.post('/ingest-document')
def ingest_document(
    payload: DocumentIngestionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    extracted = {'text_preview': payload.content[:120], 'length': len(payload.content)}
    doc = Document(
        owner_id=user.id,
        document_type=payload.document_type,
        source_name=payload.source_name,
        extracted_data=extracted,
    )
    db.add(doc)
    db.add(
        AuditLog(
            owner_id=user.id,
            module='INGESTION',
            message=f'Ingested {payload.document_type} from {payload.source_name}',
            legal_reference='Audit Trail Requirement',
            context={'source': payload.source_name},
        )
    )
    db.commit()
    return {'document_id': doc.id, 'status': 'processed', 'extracted_data': extracted}


@router.post('/classify-transactions')
def classify_transactions(
    payload: list[TransactionInput],
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = []
    for item in payload:
        tags = classify_transaction(item)
        tx = Transaction(
            owner_id=user.id,
            description=item.description,
            amount=item.amount,
            counterparty_gstin=item.counterparty_gstin,
            tags=tags,
            eligible_itc=not tags['personal'],
        )
        db.add(tx)
        results.append({'description': item.description, 'tags': tags})

    db.add(
        AuditLog(
            owner_id=user.id,
            module='CLASSIFICATION',
            message=f'Classified {len(results)} transactions',
            legal_reference='Books of Accounts Controls',
            context={'records': len(results)},
        )
    )
    db.commit()
    return {'classified': results}


@router.post('/gst')
def gst_checks(
    payload: GSTComputationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = compute_gst(payload.transactions)
    db.add(
        AuditLog(
            owner_id=user.id,
            module='GST',
            message='Validated ITC and output GST with 2A matching heuristics',
            legal_reference='GST Section 17(5), Rule 36(4)',
            context=result,
        )
    )
    db.commit()
    return result


@router.post('/tds')
def tds_checks(
    payload: TDSComputationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = compute_tds(payload.transactions)
    db.add(
        AuditLog(
            owner_id=user.id,
            module='TDS',
            message='Computed TDS obligations and prepared filing payloads',
            legal_reference='Income Tax 194C/194J/194H and GST Section 51',
            context=result,
        )
    )
    db.commit()
    return result


@router.post('/risk-score')
def risk_score(
    payload: RiskScoreRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = generate_risk_score(payload.model_dump())
    db.add(
        AuditLog(
            owner_id=user.id,
            module='ANOMALY',
            message='Generated hybrid compliance risk score',
            legal_reference='Section 44AD and advance tax provisions',
            context=result,
        )
    )
    db.commit()
    return result


@router.get('/reports/{report_type}', response_model=ReportResponse)
def generate_report(
    report_type: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = db.query(AuditLog).filter(AuditLog.owner_id == user.id).all()
    summary = [{'module': x.module, 'message': x.message, 'section': x.legal_reference} for x in logs]
    return ReportResponse(generated_at=datetime.utcnow(), report_type=report_type, payload={'audit_summary': summary})


@router.post('/simulate-filing/{form_type}')
def simulate_filing(form_type: str, payload: dict, user: User = Depends(get_current_user)):
    return {
        'form_type': form_type,
        'status': 'simulated-success',
        'reference_id': f'SIM-{user.id}-{form_type}-001',
        'payload_echo': payload,
    }
