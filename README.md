# SentinelFlow

Real-time network anomaly detection pipeline. Dockerized microservices sniff live traffic, extract flow features, score with Isolation Forest ML, and surface alerts via Streamlit dashboard.

## Stack
Python · FastAPI · scapy · scikit-learn · SQLite · Docker Compose · Streamlit

## Quick Start
```bash
git clone https://github.com/ragdevalencia11-design/SentinelFlow.git
cd SentinelFlow
docker-compose up --build
