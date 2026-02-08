import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "MechineLearning/blood_sugar_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "MechineLearning/scaler.pkl"))

def predict_blood_sugar(features):
    """
    features = [
        Age, Gender, HeartRate,
        SystolicBP, DiastolicBP,
        CK_MB, Troponin
    ]
    """
    data = np.array(features).reshape(1, -1)
    data_scaled = scaler.transform(data)
    prediction = model.predict(data)
    return prediction[0]
