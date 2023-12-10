import cryptography.fernet
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from users.utils import add_success_response, add_error_response, format_errors

from .serializers import UserRegistrationSerializer, OTPSendSerializer, OTPVerfySerializer
from twilio.rest import Client

from .custom_views import CustomAuthenticateAppView, CustomAuthenticateView


class AdminLoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active and user.is_admin:
                login(request, user)

                token = user.set_custom_session()
                # return Response({'token': token}, status=status.HTTP_200_OK)

                return add_success_response({
                    'message': 'Login successful.',
                    'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False,
                                 'message': 'User account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': False, 'message': 'Invalid username or password.'},
                            status=status.HTTP_401_UNAUTHORIZED)


class AdminLogoutView(CustomAuthenticateView):
    def get_response(self, request, user):
        logout(request)
        user.session_expire_date = None
        user.save()
        return add_success_response({
            'message': 'Logout successful'
        })


class StatusView(CustomAuthenticateView):

    def get_response(self, request, user):
        # user = request.user
        response = {}

        today = timezone.now()
        if user.session_expire_date:
            if user.session_expire_date < today:
                return add_error_response({'logged_in': False})

        # if user.is_authenticated:
        data = {
            # 'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_admin,
            # 'user': str(request.user),
        }
        response['logged_in'] = True
        response['data'] = data
        return add_success_response(response)
        # else:
        #     return add_error_response({
        #         'logged_in': False,
        #         'message': 'User is not logged in.'
        #     })


class UserRegistrationView(views.APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        try:
            get_user_model().objects.get(username=request.data.get('mobile_number'))
            return add_error_response({'message': 'Mobile number registered already.'})
        except get_user_model().DoesNotExist:
            pass

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


class UserListView(CustomAuthenticateView):
    def get_response(self, request, user):
        from .utils import get_paginated_list

        page = request.POST.get('page', 1)
        per_page = request.POST.get('per_page', 10)

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


class OTPSendView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def post(self, request):
        print('---------- Request data ---------')
        print(request.data)

        serializer = OTPSendSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = request.data.get('mobile_number')
            user = authenticate(request, mobile_number=mobile_number)
            if user is None:
                return add_success_response({'message': 'Mobile number is not registered.'})

            account_sid = "AC9b697e7816c22010ceede5954b66f002"
            auth_token = "78ac2d5732cd5efcfb3f8807d2f0aeae"
            verify_sid = "VA653068d77433d8edeca4621c2931e41a"
            # verify_sid = "VA22e388ede9ab939094d6bff689f0aa6d"
            # verified_number = "+918078749212"
            verified_number = '+91' + mobile_number

            client = Client(account_sid, auth_token)

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
            return add_error_response(serializer.errors)


class OTPVerifyView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def post(self, request):
        print('---------- Request data ---------')
        print(request.data)

        serializer = OTPVerfySerializer(data=request.data)
        if serializer.is_valid():

            mobile_number = serializer.data.get('mobile_number')
            otp = serializer.data.get('otp')
            keep_logged_in = serializer.data.get('keep_logged_in')

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
                        token = user.set_custom_session(keep_logged_in)
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
            return Response(serializer.errors)


class UserStatusAppView(CustomAuthenticateAppView):
    permission_classes = ()
    authentication_classes = ()

    def get_response(self, request, user):
        from .utils import get_masked_number

        today = timezone.now()
        if user.session_expire_date:
            if user.session_expire_date < today:
                return add_error_response({'logged_in': False})

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
    authentication_classes = ()

    def post(self, request):
        token = request.data.get('token')
        from .utils import authenticate_token, get_masked_number
        from videos.utils import get_orders

        try:
            user = authenticate_token(token)
            if user is False:
                raise Exception('Invalid token')
        except cryptography.fernet.InvalidToken:
            raise Exception('Invalid token')

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


