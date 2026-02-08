from django.http import JsonResponse
from .MechineLearning.predictor import predict_blood_sugar

# Create your views here.

def MatchPredictionView(request):
    features = [
        45,  # Age
        1,  # Gender (Male=1, Female=0)
        80,  # HeartRate
        130,  # Systolic BP
        85,  # Diastolic BP
        2.3,  # CK_MB
        0.04,  # Troponin
    ]
    result = predict_blood_sugar(features)
    return JsonResponse({"Predicted_Blood_Sugar": round(result, 2)})
