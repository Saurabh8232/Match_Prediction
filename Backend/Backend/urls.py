from django.contrib import admin
from django.urls import path
from .views import IPLPredictView, IPLMetaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', IPLPredictView.as_view(), name='ipl_predict'),
    path('meta/',    IPLMetaView.as_view(),    name='ipl_meta'),

]
