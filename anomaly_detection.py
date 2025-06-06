import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Scale features and fit IsolationForest to compute anomaly scores."""
    required_cols = ['w1w2', 'w2w3', 'luminosity']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    features = df[required_cols]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    iso = IsolationForest(contamination=0.01, random_state=42)
    iso.fit(scaled)
    scores = iso.decision_function(scaled)
    preds = iso.predict(scaled)

    result = df.copy()
    result['anomaly_score'] = scores
    result['is_outlier'] = preds == -1
    return result
