from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField, ListField
from .models import Project

# Create your views here.

class EvaluateSerializer(Serializer):
    user_identifier = CharField()
    flag_keys = ListField(child=CharField())

class EvaluateView(APIView):
    def post(self, request):
        api_key = request.headers.get("X-Api-Key")
        project = Project.objects.filter(api_key=api_key).first()


        if not project:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = EvaluateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)



        data = {}
       
        return Response(data, status=status.HTTP_200_OK)
