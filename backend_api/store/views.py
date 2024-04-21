from .models import Category, Item, Reviews
from .serializers import CategoriesSerializer
from rest_framework import generics

from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response


class CategoriesCreateApiView(generics.CreateAPIView):
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request):
        
        print(CategoriesSerializer(request.data).data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
class CategoriesListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CategoriesSerializer(queryset, many=True)
        return Response(serializer.data)
    



    
    
