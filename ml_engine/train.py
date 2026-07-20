import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path

# Generate synthetic "normal" traffic matching FlowData's 5 real fields:
# [protocol_encoded, packet_size, duration, packet_count, byte_count]
rng = np.random.default_rng(42)
n_samples = 5000

protocol = rng.integers(0, 4, n_samples)          # 0=TCP,1=UDP,2=ICMP,3=OTHER
packet_size = rng.normal(500, 150, n_samples).clip(1)
duration = rng.exponential(1.0, n_samples)
packet_count = rng.poisson(10, n_samples).clip(1)
byte_count = packet_size * packet_count

X = np.column_stack([protocol, packet_size, duration, packet_count, byte_count])

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

Path("ml-engine").mkdir(exist_ok=True)
joblib.dump(model, "ml-engine/model.pkl")
print("Model trained and saved on 5-field schema.")
