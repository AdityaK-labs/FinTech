from fastapi import FastAPI

app = FastAPI(title='Anomaly Service', version='1.0.0')


@app.post('/score')
def score(payload: dict):
    baseline = 50
    boost = min(50, payload.get('missed_tds_count', 0) * 5)
    return {'anomaly_score': baseline + boost, 'model': 'hybrid-rule-ml-v1'}


@app.get('/health')
def health():
    return {'status': 'ok'}
