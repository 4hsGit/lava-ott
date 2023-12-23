from users.utils import jwt_decode
from users.models import CustomSession
from django.http import JsonResponse


class CustomMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = ('/api/users/login/', '/admin/')

    def __call__(self, request, *args, **kwargs):
        url_path = request.path
        print('Path: ', url_path)
        x_auth = request.META.get('HTTP_XAUTH')
        print('authtoken: ', x_auth)

        if not self.is_excluded_path(url_path):
            decoded_token = jwt_decode(x_auth)
            print('decoded jwt: ', decoded_token)
            user = CustomSession.get_session(decoded_token)
            print('User sessoin: ', user)
            if user is False:
                request.is_authenticated = False
                return JsonResponse({'logged_in': False}, status=401)
            else:
                setattr(request, 'customtoken', decoded_token)
                setattr(request, 'customuser', user)
                setattr(request, 'is_authenticated', True)
                print('user: ', user)

        response = self.get_response(request)
        # response.data['logged_in'] = False
        # response.data['status'] = 500
        # print('response: ', response.data)
        return response

    def is_excluded_path(self, url_path):
        for i in self.excluded_paths:
            if url_path.startswith(i):
                print('---- Excluded ----')
                return True
