import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path

df = pd.read_csv("data/nsl-kdd/KDDTrain+..txt", header=None)
X = df.iloc[:, :-2] # Features (dropping labels)

#Train
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

Path("ml-engine").mkdir(exist_ok=True)
joblib.dump(model, "ml-engine/model.pkl")
print("Model trained and save. ")
