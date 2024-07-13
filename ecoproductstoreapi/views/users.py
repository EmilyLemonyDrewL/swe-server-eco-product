from rest_framework.decorators import api_view
from rest_framework.response import Response
from ecoproductstoreapi.models import User

@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated user in back end

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'uid': user.uid,
            'name': user.name
        }
        return Response(data)
    else:
        # This is in case the user login auth is not working
        data = { 'valid': False }
        return Response(data)
