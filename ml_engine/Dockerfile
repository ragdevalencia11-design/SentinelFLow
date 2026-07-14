FROM python:3.11-slim

WORKDIR /app

COPY ml-engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ml-engine/ ./ml-engine/
COPY shared/ ./shared/
COPY data/ ./data/

ENV PYTHONPATH=/app

CMD ["python", "ml-engine/train.py"]