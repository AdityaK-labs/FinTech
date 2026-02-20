from fastapi import FastAPI

app = FastAPI(title='Ingestion Service', version='1.0.0')


@app.post('/parse')
def parse_document(payload: dict):
    content = payload.get('content', '')
    return {
        'document_type': payload.get('document_type', 'unknown'),
        'tokens': len(content.split()),
        'entities': {
            'gstin_candidates': [],
            'invoice_numbers': [],
            'amounts': [],
        },
    }


@app.get('/health')
def health():
    return {'status': 'ok'}
