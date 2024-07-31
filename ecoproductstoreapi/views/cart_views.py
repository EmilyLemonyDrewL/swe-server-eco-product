from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ecoproductstoreapi.models import Cart, User

class CartView(ViewSet):

    def retrieve(self, request, pk):
        cart = Cart.objects.get(pk=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        
        user = User.objects.get(pk=request.data["user"])

        cart = Cart.objects.create(
            user=user,
            total=request.data["total"],
            
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        user = User.objects.get(pk=request.data["user"])
        cart = Cart.objects.get(pk=pk)
        cart.total = request.data["total"]
        cart.user = user
        cart.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','user', 'total')
        depth= 1
