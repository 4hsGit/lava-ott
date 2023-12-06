from django.shortcuts import render
import cryptography.fernet
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, OTPSendSerializer, OTPVerfySerializer
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client

from .custom_views import CustomAuthenticateAppView


class AdminLoginView(views.APIView):
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

                # token = generate_token(user)
                # return Response({'token': token}, status=status.HTTP_200_OK)

                return Response({'status': True, 'message': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False,
                                 'message': 'User account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': False, 'message': 'Invalid username or password.'},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        Response({
            'status': True,
            'message': 'Logout successful'
        })


class StatusView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        response = {
            'status': True
        }
        if user.is_authenticated:
            data = {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin,
            }
            response['logged_in'] = True
            response['data'] = data
            return Response(response)
        else:
            return Response({
                'status': False,
                'logged_in': False,
                'message': 'User is not logged in.'
            })


class UserRegistrationView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        try:
            get_user_model().objects.get(username=request.data.get('mobile_number'))
            return Response({'status': False, 'message': 'Mobile number registered already.'})
        except get_user_model().DoesNotExist:
            pass

        if serializer.is_valid():
            mob_no = request.data.get('mobile_number')
            serializer.save(username=mob_no)

            return Response({
                'status': True,
                'message': 'Registration successful',
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': False,
                'error': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(views.APIView):
    def get(self, request, *args, **kwargs):
        from .utils import get_paginated_list

        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)

        users = get_user_model().objects.all()
        data = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile_number': user.mobile_number,
            'gender': user.gender,
            'dob': user.dob.strftime('%d-%m-%Y') if user.dob else '',
            'is_subscriber': user.is_subscriber,
            'date_joined': user.date_joined.strftime('%d-%m-%Y') if user.date_joined else '',
            'is_active': user.is_active
        } for user in users]

        try:
            data = get_paginated_list(data, page, per_page)
            data['status'] = True
            data['total_count'] = users.count()
        except Exception as e:
            print('Pagination exception - ', e)
            return Response({'status': False, 'message': 'Invalid data'})

        return Response(data, status=status.HTTP_200_OK)


class OTPSendView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        print('---------- Request data ---------')
        print(request.data)

        serializer = OTPSendSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = request.data.get('mobile_number')
            user = authenticate(request, mobile_number=mobile_number)
            if user is None:
                return Response({'status': False, 'message': 'Mobile number is not registered.'})

            account_sid = "AC9b697e7816c22010ceede5954b66f002"
            auth_token = "e159554f92a409e53f093c9883bc01bb"
            verify_sid = "VA653068d77433d8edeca4621c2931e41a"
            # verify_sid = "VA22e388ede9ab939094d6bff689f0aa6d"
            # verified_number = "+918078749212"
            verified_number = '+91' + mobile_number

            client = Client(account_sid, auth_token)

            try:
                verification = client.verify.v2.services(verify_sid) \
                    .verifications \
                    .create(to=verified_number, channel="sms")
                print(verification.status)
                return Response({"status": True, "message": 'OTP sent successfully.'})
            except Exception as e:
                print('OTP send Exception - ', str(e))
                return Response({'status': False, 'message': 'Couldn\'t send otp.'})
        else:
            return Response(serializer.errors)


class OTPVerifyView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        print('---------- Request data ---------')
        print(request.data)

        serializer = OTPVerfySerializer(data=request.data)
        if serializer.is_valid():

            mobile_number = request.data.get('mobile_number')
            otp = request.data.get('otp')

            try:
                account_sid = "AC9b697e7816c22010ceede5954b66f002"
                auth_token = "e159554f92a409e53f093c9883bc01bb"
                verify_sid = "VA653068d77433d8edeca4621c2931e41a"
                # verify_sid = "VA22e388ede9ab939094d6bff689f0aa6d"
                # verified_number = "+918078749212"
                verified_number = '+91' + mobile_number

                client = Client(account_sid, auth_token)
                verification_check = client.verify.v2.services(verify_sid) \
                    .verification_checks \
                    .create(to=verified_number, code=otp)
                verification_status = verification_check.status
                print(verification_status)

                if verification_status == 'approved':
                    from .utils import generate_token
                    user = authenticate(request, mobile_number=mobile_number)
                    if user is not None:
                        token = generate_token(user)
                        response = {'status': True, 'verification_status': verification_status,
                                    'message': 'OTP Verified', 'token': token}
                    else:
                        response = {'status': False, 'message': 'Invalid mobile number'}
                else:
                    response = {'status': False, 'verification_status': verification_status, 'message': 'Invalid OTP'}
                return Response(response)
            except Exception as e:
                print('OTP verify exception = ', str(e))
                return Response({'status': False, 'message': 'Invalid OTP'})
        else:
            return Response(serializer.errors)


class UserStatusAppView(CustomAuthenticateAppView):
    def get_response(self, request, user):
        from .utils import get_masked_number
        is_subscriber = user.has_subscription()
        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile_number': get_masked_number(user),
            'is_subscriber': is_subscriber
        }
        return Response({'status': True, 'data': data})


class UserProfileView(views.APIView):
    authentication_classes = ()

    def post(self, request):
        token = request.data.get('token')
        from .utils import authenticate_token
        from videos.utils import get_orders

        try:
            user = authenticate_token(token)
            if user is False:
                raise Exception('Invalid token')
        except cryptography.fernet.InvalidToken:
            raise Exception('Invalid token')

        is_subscriber = user.has_subscription()

        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mobile_number": user.mobile_number,
            "is_subscriber": is_subscriber,
            "orders": get_orders(user)
        }
        return Response({'status': True, 'data': data})

