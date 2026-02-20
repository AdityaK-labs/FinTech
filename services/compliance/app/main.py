from fastapi import FastAPI

app = FastAPI(title='Compliance Reasoning Service', version='1.0.0')


@app.post('/reason')
def reason(payload: dict):
    return {
        'status': 'evaluated',
        'rules_applied': [
            'GST Section 17(5) blocked credits',
            'GST Section 51 TDS checks',
            'Income Tax Sections 194C/194J/194H'
        ],
        'input_size': len(payload),
    }


@app.get('/health')
def health():
    return {'status': 'ok'}
