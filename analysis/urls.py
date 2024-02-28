from django.urls import path
from .views import analyze_data, chart, form

urlpatterns = [
    path('analyze/', analyze_data, name='analyze_data'),
    path('chart/', chart, name='chart'),
    path('form/', form, name='form'),
]
