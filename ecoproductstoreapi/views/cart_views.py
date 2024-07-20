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
            
        product = Product.objects.get(pk=request.data["product"])
        user = User.objects.get(pk=request.data["user"])

        cart = Cart.objects.create(
            product=product,
            user=user,
            total=request.data["total"],
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','product', 'user', 'total')
        depth= 1
