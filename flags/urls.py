from django.urls import path
from .views import EvaluateView


urlpatterns = [
    path("api/evaluate", EvaluateView.as_view(), name="api-evaluate"),
]
