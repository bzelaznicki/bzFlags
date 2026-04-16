from django.urls import path
from .views.evaluate import EvaluateView


urlpatterns = [
    path("api/evaluate", EvaluateView.as_view(), name="api-evaluate"),
]
