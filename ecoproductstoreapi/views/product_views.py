from django.http import HttpResponseServerError
from rest_framework.views import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from ecoproductstoreapi.models import Product

class ProductView(ViewSet):
    
    def retrieve (self, request, pk):
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def list (self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create (self, request):
        
        product = Product.objects.create(
            name = request.data['name'],
            price = request.data['price'],
            description = request.data['description'],
            image = request.data['image'],
            category = request.data['category']
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update (self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.name = request.data['name']
        product.price = request.data['price']
        product.description = request.data['description']
        product.image = request.data['image']
        product.category = request.data['category']
        product.save()
        
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy (self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def in_cart(self, request, pk):
        product = self.get_object()
        product.joined = not product.joined
        product.save()
        return Response({'joined': product.joined}, status=status.HTTP_200_OK)

        
    
    @action(methods=['get'], detail=False)
    def by_category(self, request):
        category = request.query_params.get('category', None)
        if category is not None:
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'image', 'category')
