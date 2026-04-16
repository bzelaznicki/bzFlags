from django.urls import path
from .views.evaluate import EvaluateView
from .views.projects import ProjectView


urlpatterns = [
    path("api/evaluate", EvaluateView.as_view(), name="api-evaluate"),
    path("api/projects", ProjectView.as_view(), name="api-project")
]
