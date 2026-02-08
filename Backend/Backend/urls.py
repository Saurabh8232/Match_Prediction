from django.contrib import admin
from django.urls import path
from .views import BloodSugarPredictionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', BloodSugarPredictionView.as_view(), name='match_prediction'),

]
