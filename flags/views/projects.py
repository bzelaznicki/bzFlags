from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField, ModelSerializer
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from ..models import Project
from ..authentication import AdminKeyAuthentication
from ..services import regenerate_project_api_key


class ProjectSerializer(Serializer):
    name = CharField(max_length=32)

class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at', 'updated_at']

class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at', 'updated_at']

class RegeneratedApiKeyProjectDetailsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'api_key', 'created_at', 'updated_at']

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

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectDetailView(APIView):
    authentication_classes = [AdminKeyAuthentication]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        project_id = kwargs['id']
        
        project = get_object_or_404(Project, id=project_id)
        serializer = ProjectDetailSerializer(project)

        return Response(serializer.data, status=status.HTTP_200_OK) 

    def delete(self, request, *args, **kwargs):
        project_id = kwargs['id']

        project = get_object_or_404(Project, id=project_id)


        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class RegenerateProjectKeyView(APIView):
    authentication_classes = [AdminKeyAuthentication]
    permission_classes = []

    def post(self, request, *args, **kwargs):
        project_id = kwargs['id']

        project = get_object_or_404(Project, id=project_id)
        
        project = regenerate_project_api_key(project)

        serializer = RegeneratedApiKeyProjectDetailsSerializer(project)

        return Response(serializer.data, status=status.HTTP_200_OK)
