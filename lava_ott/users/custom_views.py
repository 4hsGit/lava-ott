from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import authenticate_token


class CustomAuthenticateAppView(APIView):
    def get_response(self, request, user):
        raise NotImplementedError

    def post(self, request):
        token = request.data.get('token')
        user = authenticate_token(token)
        if user is False:
            return Response({'status': False, 'message': 'Invalid token.'})

        return self.get_response(request, user)
