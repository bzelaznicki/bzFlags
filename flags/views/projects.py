from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField
from ..models import Project
from django.conf import settings
from django.db.utils import IntegrityError

class ProjectSerializer(Serializer):
    name = CharField()


class ProjectView(APIView):
    def post(self, request):
        admin_key = request.headers.get("X-Admin-Key")

        if not admin_key or admin_key != settings.ADMIN_SECRET_KEY:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            project = Project.objects.create(name=serializer.validated_data['name'])
        except IntegrityError:
            return Response({"details": "A project with this name already exists"}, status=status.HTTP_409_CONFLICT)
            


        response = {
            'id': project.id,
            'name': project.name,
            'api_key': project.api_key,
            'created_at': project.created_at,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
