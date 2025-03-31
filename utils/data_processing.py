import pandas as pd

def encode_feature(value: str, code_map: pd.DataFrame) -> int:
    try:
        return code_map[code_map.iloc[:, 0] == value].iloc[0, 1]
    except:
        return -1  # Unknown category

def calculate_risk_score(transaction, model, email_codes, location_codes):
    risk_score = 0
    
    # Rule-based scoring
    if transaction.ip_address in ["192.168.1.1", "10.0.0.1"]:
        risk_score += 50
    if transaction.transaction_amount > 1000:
        risk_score += 20
    if "temp.com" in transaction.email:
        risk_score += 30
    if "outlook.com" in transaction.email:
        risk_score += 10
    if len(transaction.phone_number) < 10:
        risk_score += 50
    if any(char.isalpha() for char in transaction.phone_number):
        risk_score += 50
    
    # Model prediction
    email_encoded = encode_feature(transaction.email, email_codes)
    location_encoded = encode_feature(transaction.location, location_codes)
    
    if email_encoded != -1 and location_encoded != -1:
        prob_fraud = model.predict_proba([
            [transaction.transaction_amount, email_encoded, location_encoded]
        ])[0][1]
        risk_score += int(prob_fraud * 40)
    
    risk_level = "High" if risk_score > 70 else "Medium" if risk_score > 30 else "Low"
    return min(100, risk_score), risk_level