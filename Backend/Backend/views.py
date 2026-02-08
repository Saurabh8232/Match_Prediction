from rest_framework.views import APIView
from rest_framework.response import Response
from .MechineLearning.predictor import predict_blood_sugar

# Create your views here.
class BloodSugarPredictionView(APIView):
    def post(self, request):
        data = request.data
        features = [
            data["age"],
            data["gender"],
            data["heart_rate"],
            data["systolic_bp"],
            data["diastolic_bp"],
            data["ck_mb"],
            data["troponin"],
        ]
        prediction = predict_blood_sugar(features)
        return Response({"prediction": round(prediction, 2)})
