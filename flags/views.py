from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField, ListField
from .models import Project, Flag, FlagOverride
from .services import evaluate_flag

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

        flag_data = serializer.validated_data

        flags = Flag.objects.filter(key__in=flag_data["flag_keys"], project=project)  
            

        flag_ids = [f.id for f in flags]
        overrides_qs = FlagOverride.objects.filter(
            flag_id__in=flag_ids,
            user_identifier=flag_data["user_identifier"]
        ).select_related('flag')
        override_by_flag = {o.flag_id: o for o in overrides_qs}

        data = {}


        for flag in flags:

            overrides = {}
            override = override_by_flag.get(flag.id)
            
            if override:
                overrides[flag_data["user_identifier"]] = override.enabled
                
            
            data[flag.key] = evaluate_flag(
                flag_enabled=flag.enabled,
                rollout_percentage=flag.rollout_percentage,
                user_identifier=flag_data["user_identifier"],
                flag_key=flag.key,
                overrides=overrides)


       
        return Response(data, status=status.HTTP_200_OK)
