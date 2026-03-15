from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .MechineLearning.predictor import predict_score_and_wickets, get_meta


class IPLPredictView(APIView):

    REQUIRED_FIELDS = [
        "batting_team", "bowling_team", "venue", "pitch_condition",
        "current_score", "overs_completed", "wickets_out",
        "runs_last_5_overs", "overs_remaining", "run_rate",
    ]

    def post(self, request):
        data = request.data

        # ── Validation ─────────────────────────────────────────────────────────
        missing = [f for f in self.REQUIRED_FIELDS if f not in data or data[f] == ""]
        if missing:
            return Response(
                {"error": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = predict_score_and_wickets(
                batting_team      = data["batting_team"],
                bowling_team      = data["bowling_team"],
                venue             = data["venue"],
                pitch_condition   = data["pitch_condition"],
                current_score     = data["current_score"],
                overs_completed   = data["overs_completed"],
                wickets_out       = data["wickets_out"],
                runs_last_5_overs = data["runs_last_5_overs"],
                overs_remaining   = data["overs_remaining"],
                run_rate          = data["run_rate"],
            )
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Prediction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IPLMetaView(APIView):
    
    def get(self, request):
        try:
            return Response(get_meta(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
