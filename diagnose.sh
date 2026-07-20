#!/bin/bash
echo "===== SENTINELFLOW DIAGNOSTIC ====="

echo -e "\n[1] Are all containers running?"
docker-compose ps

echo -e "\n[2] Does the model file exist and have real size?"
ls -la ml-engine/model.pkl 2>&1

echo -e "\n[3] Does alerts.db exist and have tables?"
docker exec sentinelflow-api-1 python3 -c "
import sqlite3
conn = sqlite3.connect('/app/api/alerts.db')
print('Tables:', conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall())
conn.close()
" 2>&1

echo -e "\n[4] Is the API's /health endpoint responding?"
curl -s http://localhost:8000/health

echo -e "\n[5] Is the API's /predict endpoint working? (manual test flow)"
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"src_ip":"1.1.1.1","dst_ip":"2.2.2.2","src_port":1234,"dst_port":80,"protocol":"TCP","packet_size":500,"duration":1.0,"packet_count":5,"byte_count":2500}'

echo -e "\n[6] Is the collector process alive inside its container?"
docker exec sentinelflow-collector-1 ps aux 2>&1

echo -e "\n[7] What does the collector's own error log show (last 20 lines)?"
docker logs sentinelflow-collector-1 --tail 20

echo -e "\n[8] Does the dashboard container see the same DB file?"
docker exec sentinelflow-dashboard-1 ls -la /app/api/alerts.db 2>&1

echo -e "\n===== DIAGNOSTIC COMPLETE ====="
