from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Person, Product, PurchasedItem
from .serializers import PersonSerializer, ProductSerializer, PurchasedItemSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        try:
            name = request.query_params.get('query', '')
            person = Person.objects.filter(name__icontains=name)
            serializer = self.get_serializer(person, many=True)

            if not name:
                return Response({
                    'result': 'error',
                    'detail': 'Por favor, ingrese el nombre de la persona'
                }, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data:
                return Response({
                    'result': 'ok',
                    'detail': 'Persona(s) encontrada(s)',
                    'results': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'result': 'error',
                    'detail': 'Persona no encontrada'
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            print('exception', ex.__str__())
            return Response({
                'result': 'error',
                'detail': 'No se pudo procesar la solicitud',
                'message': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        try:
            name = request.query_params.get('query', '')
            product = Product.objects.filter(name__icontains=name)
            serializer = self.get_serializer(product, many=True)

            if not name:
                return Response({
                    'result': 'error',
                    'detail': 'Por favor, ingrese el nombre del producto'
                }, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data:
                return Response({
                    'result': 'ok',
                    'detail': 'Producto(s) encontrado(s)',
                    'results': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'result': 'error',
                    'detail': 'Producto no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({
                'result': 'error',
                'detail': 'No se pudo procesar la solicitud',
                'message': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)


class PurchasedItemViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = PurchasedItem.objects.all()
    serializer_class = PurchasedItemSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'productId', 'quantity'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la persona'),
            'productId': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad del producto')
        },
    ))
    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('productId')
            quantity = int(request.data.get('quantity'))
            email = request.data.get('email')

            if not product_id or not quantity or not email:
                return Response({
                    'result': 'error',
                    'detail': 'Debe llenar todos los campos'
                }, status=status.HTTP_404_NOT_FOUND)

            product = Product.objects.get(id=product_id)
            person = Person.objects.get(email=email)

            if product.stock < quantity:
                return Response({
                    'result': 'error',
                    'detail': 'Stock insuficiente para el producto'
                }, status=status.HTTP_400_BAD_REQUEST)

            product.stock -= quantity
            product.save()

            PurchasedItem.objects.create(person=person, product=product, quantity=quantity)
            return Response({
                'result': 'ok',
                'detail': 'Compra exitosa'
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({
                'result': 'error',
                'detail': 'Producto no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        except Person.DoesNotExist:
            return Response({
                'result': 'error',
                'detail': 'Persona no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({
                'result': 'error',
                'detail': 'No se pudo procesar la solicitud',
                'message': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)
