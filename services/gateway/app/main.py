from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers import auth, compliance

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Compliance Gateway', version='1.0.0')
app.include_router(auth.router)
app.include_router(compliance.router)


@app.get('/health')
def health():
    return {'status': 'ok'}
