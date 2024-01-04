import cryptography.fernet
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone
from .utils import add_success_response, add_error_response, format_errors

from .serializers import (
    UserRegistrationSerializer,
    OTPSendSerializer,
    OTPVerfySerializer,
    RegistrationOTPVerfySerializer,
)

from .models import CustomSession


class AdminLoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        from .utils import jwt_encode
        from users.models import CustomSession

        CustomSession.delete_expired_sessions()

        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            return add_error_response({
                'error': 'Both username and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active and user.is_admin:
                from users.models import CustomSession
                token = CustomSession.set_session(user)
                token = jwt_encode(token)

                return add_success_response({
                    'message': 'Login successful.',
                    'token': token
                }, status=status.HTTP_200_OK)
            else:
                return add_error_response({
                    'message': 'User account is not active.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return add_error_response({
                'message': 'Invalid username or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class AdminLogoutView(views.APIView):
    def get(self, request):
        CustomSession.delete_session(request.customtoken)
        return add_success_response({
            'message': 'Logout successful'
        })


class StatusView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        response = {}
        user = request.customuser
        customtoken = request.customtoken
        is_authenticated = request.is_authenticated
        print('customuser: ', user)
        print('customtoken: ', customtoken)
        print('is_authenticated: ', is_authenticated)
        if request.is_authenticated is True:
            data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin,
                # 'user': str(request.user),
            }
            response['logged_in'] = True
            response['data'] = data
            return add_success_response(response)
        else:
            return add_error_response({
                'logged_in': False,
                'message': 'User is not logged in.'
            })


class UserRegistrationView(views.APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        mob_no = request.data.get('mobile_number')
        from django.db.models import Q
        user_exists = get_user_model().objects.filter(
            Q(username=mob_no) | Q(mobile_number=mob_no))
        if user_exists:
            return add_error_response({'message': 'Mobile number registered already.'})

        if serializer.is_valid():
            req_data = serializer.validated_data

            mob_no = req_data.get('mobile_number')
            otp = req_data.get('otp')
            from .otp import valdiate_otp
            if valdiate_otp(mob_no, otp) is False:
                return add_error_response({'error': 'Invalid OTP'})
            serializer.validated_data.pop('otp')
            serializer.save(username=mob_no)

            return add_success_response({
                'message': 'Registration successful',
            }, status=status.HTTP_201_CREATED)
        else:
            return add_error_response({
                'error': format_errors(serializer.errors),
            }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(views.APIView):
    def get(self, request):
        from .utils import get_paginated_list

        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)

        users = get_user_model().objects.all()
        data = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'mobile_number': user.mobile_number,
            'gender': user.gender,
            'dob': user.dob.strftime('%d-%m-%Y') if user.dob else '',
            'is_subscriber': user.is_subscriber,
            'date_joined': user.date_joined.strftime('%d-%m-%Y') if user.date_joined else '',
            'is_active': user.is_active
        } for user in users]

        try:
            data = get_paginated_list(data, page, per_page)
            data['total_count'] = users.count()
        except Exception as e:
            print('Pagination exception - ', e)
            return add_error_response({'message': 'Invalid data'})

        return add_success_response(data, status=status.HTTP_200_OK)


class AppLoginOTPSendView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        print('---------- Request data ---------')
        print(request.data)

        serializer = OTPSendSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = request.data.get('mobile_number')
            user = authenticate(request, mobile_number=mobile_number)
            if user is None:
                return add_error_response({'message': 'Mobile number is not registered.'})

            account_sid = "AC9b697e7816c22010ceede5954b66f002"
            auth_token = "78ac2d5732cd5efcfb3f8807d2f0aeae"
            verify_sid = "VA653068d77433d8edeca4621c2931e41a"
            # verify_sid = "VA22e388ede9ab939094d6bff689f0aa6d"
            # verified_number = "+918078749212"
            verified_number = '+91' + mobile_number

            # client = Client(account_sid, auth_token)

            try:
                # verification = client.verify.v2.services(verify_sid) \
                #     .verifications \
                #     .create(to=verified_number, channel="sms")
                # print(verification.status)
                return add_success_response({"message": 'OTP sent successfully.'})
            except Exception as e:
                print('OTP send Exception - ', str(e))
                return add_error_response({'message': 'Couldn\'t send otp.'})
        else:
            return add_error_response(format_errors(serializer.errors), status=400)


class AppLoginView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        from users.utils import jwt_encode
        print('---------- Request data ---------')
        print(request.data)

        serializer = OTPVerfySerializer(data=request.data)
        if serializer.is_valid():

            mobile_number = serializer.data.get('mobile_number')
            otp = serializer.data.get('otp')
            keep_me_logged_in = serializer.data.get('keep_me_logged_in')

            print('keep_me_logged_in: ', keep_me_logged_in)

            try:
                account_sid = "AC9b697e7816c22010ceede5954b66f002"
                auth_token = "e159554f92a409e53f093c9883bc01bb"
                verify_sid = "VA653068d77433d8edeca4621c2931e41a"
                # verify_sid = "VA22e388ede9ab939094d6bff689f0aa6d"
                # verified_number = "+918078749212"
                verified_number = '+91' + mobile_number

                # client = Client(account_sid, auth_token)
                # verification_check = client.verify.v2.services(verify_sid) \
                #     .verification_checks \
                #     .create(to=verified_number, code=otp)
                # verification_status = verification_check.status
                # print(verification_status)
                verification_status = 'approved'

                if verification_status == 'approved' and str(otp) == '123456':

                    user = authenticate(request, mobile_number=mobile_number)
                    if user is not None:
                        CustomSession.delete_expired_sessions()

                        token = CustomSession.set_session(user, session_type='app', keep_me_logged_in=keep_me_logged_in)
                        token = jwt_encode(token)
                        response = {'status': 'success', 'verification_status': verification_status,
                                    'message': 'OTP Verified', 'token': token}
                    else:
                        response = {'status': 'error', 'message': 'Invalid mobile number'}
                else:
                    response = {'status': 'error', 'verification_status': verification_status, 'message': 'Invalid OTP'}
                return Response(response)
            except Exception as e:
                print('OTP verify exception = ', str(e))
                return Response({'status': 'error', 'message': 'Invalid OTP'})
        else:
            return add_error_response(format_errors(serializer.errors), status=400)


class OTPSendView(views.APIView):
    def post(self, request):
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            # mobile_number = serializer.data.get('mobile_number')
            return Response({
                "status": "success",
                "message": "OTP sent",
                # "mobile_number": mobile_number
            })
        else:
            return add_error_response(format_errors(serializer.errors), status=400)


class OTPVerifyView(views.APIView):
    def post(self, request):
        serializer = RegistrationOTPVerfySerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.data.get('mobile_number')
            otp = serializer.data.get('otp')

            if str(otp) == '123456':
                return add_success_response({
                    "message": "OTP verified",
                    "mobile_number": mobile_number
                })
            else:
                return add_error_response({
                    'message': 'Invalid OTP'
                })
        else:
            return add_error_response(serializer.errors)


class UserStatusAppView(views.APIView):

    def get(self, request):
        from .utils import get_masked_number
        user = request.customuser

        is_subscriber = user.has_subscription()
        data = {
            # 'id': user.id,
            # 'first_name': user.first_name,
            # 'last_name': user.last_name,
            'mobile_number': get_masked_number(user),
            'is_subscriber': is_subscriber,
        }
        return add_success_response({'logged_in': True, 'data': data})


class UserProfileView(views.APIView):

    def post(self, request):
        user = request.customuser
        from .utils import get_masked_number
        from videos.utils import get_orders

        is_subscriber = user.has_subscription()

        data = {
            # "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobile_number": get_masked_number(user),
            "is_subscriber": is_subscriber,
            "orders": get_orders(user)
        }
        return add_success_response({'data': data})


def test_delete_view(request):
    from django.http import HttpResponseServerError, JsonResponse
    from django.apps import apps
    app = request.GET.get('app')
    model = request.GET.get('model')
    mobile_number = request.GET.get('mobile_number')
    field = request.GET.get('field')
    value = request.GET.get('value')

    try:
        obj = None
        if model == 'user':
            model = apps.get_model('users', 'user')
            obj = get_user_model().objects.get(mobile_number=mobile_number)
        if model == 'order':
            model = apps.get_model('videos', 'order')
            user = get_user_model().objects.get(mobile_number=mobile_number)
            obj = model.objects.filter(user=user)

        obj.delete()
        return JsonResponse({'status': 'success', 'message': 'Deleted.'})

    except:
        return HttpResponseServerError('Something went wrong!')
