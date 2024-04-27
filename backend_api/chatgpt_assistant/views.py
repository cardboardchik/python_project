from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from store.models import Category, Item
from store.serializers import CategoriesSerializer, ItemSerializer

from .chatgpt_assistant import cahtgpt_assistant

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
@extend_schema_view(get=extend_schema(
        parameters=[ 
            OpenApiParameter(name='prompt', description='prompt', type=str),
        ]
    )
)
class ChatGptAssistantApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if self.request.query_params.get('prompt'):
            prompt = self.request.query_params.get('prompt')
        else:
            return Response({"error": "empty prompt string"}, status=status.HTTP_400_BAD_REQUEST)
        
        categories = [cat.name for cat in Category.objects.all()]

        response = cahtgpt_assistant(categories=categories, user_prompt=prompt)
        categories_m = CategoriesSerializer(Category.objects.filter(name__in=response["categories"]), many=True).data
        for i in range(len(categories_m)):
            categories_m[i]["items"] = ItemSerializer(Item.objects.filter(category_id=categories_m[i]["id"]).order_by("?")[:2], many=True).data
        response['categories'] = categories_m
        return Response(response)
