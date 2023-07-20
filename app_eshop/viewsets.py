from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Person, Product, PurchasedItem
from .serializers import PersonSerializer, ProductSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('query', None)
        if name is not None:
            queryset = Person.objects.filter(name__icontains=name)
            serializer = PersonSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "No query provided for search"}, status=400)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('query', None)
        if name is not None:
            queryset = Product.objects.filter(name__icontains=name)
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "No query provided for search"}, status=400)


@api_view(['POST'])
def create_cart(request):
    pass
