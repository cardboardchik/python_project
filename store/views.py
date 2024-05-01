from .models import Category, Item, Reviews
from .serializers import CategoriesSerializer, ItemSerializer, ReviewSerializer
from rest_framework import generics, viewsets, serializers
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, inline_serializer
import requests
from bs4 import BeautifulSoup

# class CategoriesCreateApiView(generics.CreateAPIView):
#     serializer_class = CategoriesSerializer
#     permission_classes = (IsAdminUser,)

#     def create(self, request):
#         print(CategoriesSerializer(request.data).data)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data)
    
class CategoriesListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CategoriesSerializer(queryset, many=True)
        return Response(serializer.data)
    
@extend_schema_view(get=extend_schema(
        parameters=[ 
            OpenApiParameter(name='filters', description='filters (separate by , )', type=str, enum=[i.name for i in Category.objects.all()], style="form", explode=False, many=True),
        ]
    )
)
class ItemListApiView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        if self.request.query_params.get('filters'):
            filters = list(self.request.query_params.get('filters').split(','))
            queryset = Item.objects.filter(category__name__in=filters)
        else:
            queryset = Item.objects.all()
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ItemApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            reviews = Reviews.objects.filter(item=item.id)
            serializer_item = ItemSerializer(item).data
            serializer_reviews = ReviewSerializer(reviews, many=True)
            serializer_item["reviews"] = serializer_reviews.data
            return Response(serializer_item)
        except:
            return Response({"error: the item doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


class ReviewApiView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(request=inline_serializer(
        name="Reviews",
        fields={
            "rating": serializers.IntegerField(),
            "text": serializers.CharField(),
            "item": serializers.IntegerField(),
        },
    ), responses=ReviewSerializer)
    def post(self, request):
        
        review = Reviews.objects.filter(user=request.user.id, item=request.data['item'])
        if review:
            return Response({"error": "you cannot leave more than one review for this product"}, status=status.HTTP_400_BAD_REQUEST)
        review = Reviews.objects.create(rating=request.data['rating'], text=request.data['text'], item_id=request.data['item'], user_id=request.user.id)
        return Response(ReviewSerializer(review).data)
    

    
    
