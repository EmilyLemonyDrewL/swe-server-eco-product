from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ecoproductstoreapi.models import Cart, Product, User, CartProducts
from .product_views import ProductSerializer
from .cart_product_views import CartProductSerializer

class CartView(ViewSet):

    def retrieve(self, request, pk):
        cart = Cart.objects.get(pk=pk)

        cartproduct_id = CartProducts.objects.filter(cart=cart.pk)
        products = []
        for product in cartproduct_id:
            products.append(product.product_id)
        cart.products = Product.objects.filter(pk__in=products)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        product = Product.objects.get(pk=request.data["product"])
        user = User.objects.get(pk=request.data["user"])

        cart = Cart.objects.create(
            product=product,
            user=user,
            total=request.data["total"],
            quantity=request.data.get("quantity", 1)
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        product = Product.objects.get(pk=request.data["product"])
        user = User.objects.get(pk=request.data["user"])

        cart = Cart.objects.get(pk=pk)
        cart.total = request.data["total"]
        cart.quantity = request.data["quantity"]
        cart.user = user
        cart.product = product
        cart.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProducts
        fields = ('product', 'cart')
class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cart_products', many=True)
    class Meta:
        model = Cart
        fields = ('id', 'user', 'total', 'products')
        depth= 1
