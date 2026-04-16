from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField
from django.db.utils import IntegrityError

from ..models import Project
from ..authentication import AdminKeyAuthentication


class ProjectSerializer(Serializer):
    name = CharField()


class ProjectView(APIView):
    authentication_classes = [AdminKeyAuthentication]
    permission_classes = []

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = Project.objects.create(
                name=serializer.validated_data["name"]
            )
        except IntegrityError:
            return Response(
                {"detail": "A project with this name already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        response = {
            "id": project.id,
            "name": project.name,
            "api_key": project.api_key,
            "created_at": project.created_at,
        }
        return Response(response, status=status.HTTP_201_CREATED)   
