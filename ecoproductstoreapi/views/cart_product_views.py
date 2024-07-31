from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ecoproductstoreapi.models import Cart, Product, CartProducts


class CartProductView(ViewSet):

    def retrieve(self, request, pk):
        cart_product = CartProducts.objects.get(pk=pk)
        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        cart_products = CartProducts.objects.all()
        serializer = CartProductSerializer(cart_products, many=True)
        response_data = serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cart = Cart.objects.get(pk=request.data['cart'])
        product = Product.objects.get(pk=request.data['product'])

        cart_product = CartProducts.objects.create(
            cart=cart,
            product=product
        )

        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        cart_product = CartProducts.objects.get(pk=pk)
        cart = Cart.objects.get(pk=request.data['cartId'])
        product = Product.objects.get(pk=request.data['productId'])

        cart_product.cart = cart
        cart_product.product = product

        cart_product.save()
        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, pk):
        cart_product = CartProducts.objects.get(pk=pk)
        cart_product.delete()
        return Response('Cart product deleted', status=status.HTTP_204_NO_CONTENT)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'cart', 'product')
