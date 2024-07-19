from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ecoproductstoreapi.models import Cart, Product, User

class CartView(ViewSet):

    def retrieve(self, request, pk):
        cart_view = Cart.objects.get(pk=pk)
        serializer = CartSerializer(cart_view)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        cart_views = Cart.objects.all()
        serializer = CartSerializer(cart_views, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
            
        products = Product.objects.get(uid=request.data["productId"])
        user = User.objects.get(pk=request.data["user"])

        cart = Cart.objects.create(
            products=products,
            user_id=user,
            total=request.data["total"],
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('products', 'user_id', 'total')
