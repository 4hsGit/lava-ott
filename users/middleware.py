from users.utils import jwt_decode
from users.models import CustomSession, Project
from django.http import JsonResponse
from django.urls import resolve


class CustomMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = ('/api/users/login/',
                               '/lvadmin/',
                               '/api/users/setproject/',
                               '/api/users/setadmin/',
                               '/api/users/app/registration/',
                               '/api/users/otp-send/',
                               '/api/users/delete-otp-verify/',
                               '/api/users/app/login/',
                               '/api/users/app/login-otp-send/',
                               '/api/users/app/login-otp-verify/',
                               '/api/videos/app-change-order-period/',
                               '/lavaott-media/',

                               # Payment
                               # '/payment/'
                               '/payment/response/'
                               )
        self.admin_paths = [
            '/api/users/setproject/',
            '/api/users/setadmin/',
        ]

    def check_server_status(self):
        try:
            Project.objects.get(field1=True)
        except:
            raise Exception('Server Error')

    def __call__(self, request, *args, **kwargs):

        # To raise not found exception
        url_path = request.path
        resolve(url_path)
        # --------------------------- #

        # print('Path: ', url_path)
        if not url_path.startswith('/lvadmin'):
            if url_path not in self.admin_paths:
                self.check_server_status()

        if not self.is_excluded_path(url_path):

            # x_auth = request.META.get('HTTP_XAUTH')
            x_auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IkdGWTVPcEpFNnlNdVN1dG5LdFBFN29CWk1lU2hRc24xZm1OYTdHT0lsNk09IiwiaWF0IjoxNzQwNTgyODY0fQ.C4ru6a3he3MHyCwu4C45zzSZYhhZy0BUPjThTiHIekU'
            # print('authtoken: ', x_auth)
            if x_auth is None:
                return JsonResponse({'logged_in': False, 'message': 'No token found'}, status=401)

            decoded_token = jwt_decode(x_auth)
            # print('decoded jwt: ', decoded_token)
            user = CustomSession.get_session(decoded_token)
            # print('User sessoin: ', user)
            if user is False:
                request.is_authenticated = False
                return JsonResponse({'logged_in': False, 'message': 'Session expired or invalid token'}, status=401)
            else:
                setattr(request, 'customtoken', decoded_token)
                setattr(request, 'customuser', user)
                setattr(request, 'is_authenticated', True)
                # print('user: ', user)

        response = self.get_response(request)
        # response.data['logged_in'] = False
        # response.data['status'] = 500
        # print('response: ', response.data)
        return response

    def is_excluded_path(self, url_path):
        for i in self.excluded_paths:
            if url_path.startswith(i):
                # print('---- Excluded ----')
                return True
