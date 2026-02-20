FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi==0.111.0 uvicorn==0.30.1
COPY app /app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
