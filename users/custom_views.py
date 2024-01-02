from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import authenticate_token


class CustomAuthenticateView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_response(self, request, user):
        raise NotImplementedError

    def post(self, request):
        token = request.data.get('token')

        user = authenticate_token(token)

        if user is False:
            return Response({'status': 'error', 'logged_in': False, 'error': 'Invalid token.'})

        if user.is_admin is False:
            return Response({'status': 'error', 'logged_in': False, 'error': 'Permission denied'})

        return self.get_response(request, user)


class CustomAuthenticateAppView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_response(self, request, user):
        raise NotImplementedError

    def post(self, request):
        token = request.data.get('token')

        user = authenticate_token(token)

        if user is False:
            return Response({'status': 'error', 'logged_in': False, 'message': 'Invalid token.'})

        return self.get_response(request, user)

