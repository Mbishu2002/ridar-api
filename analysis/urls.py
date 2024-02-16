from django.urls import path
from .views import analyze_data

urlpatterns = [
    path('analyze/', analyze_data, name='analyze-data'),
]
