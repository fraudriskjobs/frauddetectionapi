import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_model():
    data = {
        "email": ["fraud@temp.com", "safe@gmail.com", "risk@outlook.com"],
        "amount": [2000, 100, 1500],
        "location": ["NG", "US", "RU"],
        "is_fraud": [1, 0, 1]
    }
    df = pd.DataFrame(data)
    
    df["email_encoded"] = df["email"].astype("category").cat.codes
    df["location_encoded"] = df["location"].astype("category").cat.codes
    
    model = RandomForestClassifier(
        n_estimators=5,
        max_depth=3,
        min_samples_leaf=10,
        random_state=42
    )
    model.fit(df[["amount", "email_encoded", "location_encoded"]], df["is_fraud"])
    
    joblib.dump(model, "fraud_model.pkl", compress=3)
    df[["email", "email_encoded"]].to_csv("email_codes.csv", index=False)
    df[["location", "location_encoded"]].to_csv("location_codes.csv", index=False)

def load_model():
    try:
        model = joblib.load("fraud_model.pkl")
        email_codes = pd.read_csv("email_codes.csv")
        location_codes = pd.read_csv("location_codes.csv")
        return model, email_codes, location_codes
    except FileNotFoundError:
        train_model()
        return load_model()