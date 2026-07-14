from datetime import datetime
from schemas import FlowData, Prediction, Alert, Severity, Status
from databse import init_db, insert_prediction, insert_alert, get_alerts

# 1.Fake network flow
