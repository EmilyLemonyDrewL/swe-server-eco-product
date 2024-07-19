from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from ecoproductstoreapi.models import Product, Category

class ProductView(ViewSet):
    
    def retrieve (self, request, pk):
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def list (self, request):
        category_id = request.query_params.get('category', None)
        if category_id is not None:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        if 'product_image' not in request.data:
            raise serializers.ValidationError({'product_image': 'This field is required.'})
        
        category_id = request.data['category']
        category = Category.objects.get(pk=category_id)
        
        product = Product.objects.create(
            name=request.data['name'],
            price=request.data['price'],
            description=request.data['description'],
            product_image=request.data['product_image'],
            category=category
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if 'product_image' not in request.data:
            raise serializers.ValidationError({'product_image': 'This field is required.'})

        category_id = request.data['category']
        category = Category.objects.get(pk=category_id)

        product.name = request.data['name']
        product.price = request.data['price']
        product.description = request.data['description']
        product.product_image = request.data['product_image']
        product.category = category
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy (self, request, pk):
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
        fields = ('id', 'name', 'price', 'description', 'product_image', 'category')
