from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserProfileSerializer
from drf_spectacular.utils import extend_schema


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses=UserProfileSerializer)
    def get(self, request):
        """
        Get User Profile
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
