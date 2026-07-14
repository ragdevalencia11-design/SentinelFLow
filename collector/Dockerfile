FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpcap-dev && rm -rf /var/lib/apt/lists/*
COPY collector/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY collector/ ./collector/
COPY shared/ ./shared/
COPY ml_engine/features.py ./
ENV PYTHONPATH=/app
CMD ["python", "-u", "collector/collector.py"]
