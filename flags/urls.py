from django.urls import path
from .views.evaluate import EvaluateView
from .views.projects import ProjectView, ProjectDetailView, RegenerateProjectKeyView


urlpatterns = [
    path("api/evaluate", EvaluateView.as_view(), name="api-evaluate"),
    path("api/projects", ProjectView.as_view(), name="api-project"),
    path("api/projects/<uuid:id>", ProjectDetailView.as_view(), name="api-project-single"),
    path("api/projects/<uuid:id>/regenerate-key", RegenerateProjectKeyView.as_view(), name="api-project-key-regenerate")
]
