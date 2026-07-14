import joblib
import numpy as np
from ml_engine.features import extract_features
from shared.schemas import FlowData, Prediction
from datetime import datetime

# Load trained model once at startup
model = joblib.load("ml_engine/model.pkl")

def predict_flow(flow: FlowData) -> Prediction:
    features = extract_features(flow).reshape(1, -1)
    score = model.decision_function(features)[0]
    is_anomaly = model.predict(features)[0] == -1
    
    return Prediction(
        flow_id=hash(f"{flow.src_ip}:{flow.dst_ip}:{datetime.utcnow().isoformat()}"),
        timestamp=datetime.utcnow(),
        anomaly_score=float(-score),
        is_anomaly=is_anomaly,
        confidence=min(abs(score) * 2, 1.0)
    )
