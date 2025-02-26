from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth

from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from django.http import JsonResponse

from .models import Transaction
from videos.models import Order
from django.conf import settings


test_config = {
    "key_id": 'rzp_test_8WbpTdlodzPfrX',
    "key_secret": 'ePOFb4Erm2znCYGJnkFDlgrO'
}

live_config = {
    "key_id": 'rzp_test_8WbpTdlodzPfrX',
    "key_secret": 'ePOFb4Erm2znCYGJnkFDlgrO'
}

url_config = settings.PAYMENT_URL_CONFIG


class PaymentCheckoutTestView(APIView):
    def get_key_config(self):
        return test_config

    def get_order_id(self):
        order_id = self.request.POST.get('id', 1)
        if not order_id:
            order_id = self.request.GET.get('id', None)
        return order_id

    def get(self, request):
        try:
            order_id = self.get_order_id()

            try:
                order_obj = Order.objects.get(id=order_id)
            except:
                return JsonResponse({'message': 'Invalid Order'})

            amount = int(order_obj.subscription_amount)

            payload = {
                "amount": int(str(amount) + '00'), # Need to add two zeros at end, since it converts the last two digits to decimal
                # "amount": int(amount), # Need to add two zeros at end, since it converts the last two digits to decimal
                "currency": "INR",
                "receipt": Transaction.generate_receipt()
            }
            headers = {'Content-Type': 'application/json'}
            config = self.get_key_config()
            response = requests.post('https://api.razorpay.com/v1/orders',
                                     json=payload, headers=headers,
                                     auth=HTTPBasicAuth(config['key_id'], config['key_secret'])
                                     )

            print('------------- Checkout Response ------------')
            print('status code : ', response.status_code)
            from json import loads
            print('response : ', response.text)

            print('------------- Checkout Response End ------------')
            res_dict = loads(response.text)

            # Error Response
            if 'error' in res_dict:
                msg = res_dict['error']['description'] if 'description' in res_dict['error'] else ''
                return render(request, 'error.html', {'err_msg': msg})
            # ------------ #

            # return JsonResponse({'message': res_dict})

            # Save to Transaction Table
            transaction = Transaction()
            transaction.razorpay_order_id = res_dict.get('id')
            transaction.amount = amount
            transaction.amount_due = res_dict.get('amount_due')
            transaction.amount_paid = res_dict.get('amount_paid')
            transaction.attempts = res_dict.get('attempts')
            transaction.created_at = res_dict.get('created_at')
            transaction.currency = res_dict.get('currency')
            transaction.entity = res_dict.get('entity')
            transaction.offer_id = res_dict.get('offer_id')
            transaction.receipt = res_dict.get('receipt')
            transaction.status = res_dict.get('status')
            transaction.order = order_obj
            transaction.save()

            res_dict.update({
                'key_id': config['key_id'],
                'response_url': url_config['response_url'],
                # 'name': request.customuser if request.customuser else '',
                'contact': request.customuser.mobile_number if request.customuser else '',
            })

            # return render(self.request, 'checkout1.html', context={'data': res_dict})
            return render(self.request, 'checkout.html', context={'data': res_dict})
        except Exception as e:
            print(str(e))


class PaymentResponseView(APIView):
    def post(self, request):
        response_data = request.POST.dict()

        # Payment Failed
        if 'error[code]' in response_data:
            from json import loads

            error_description = response_data.get('error[description]')
            error_source = response_data.get('error[source]')
            error_step = response_data.get('error[step]')
            error_reason = response_data.get('error[reason]')
            error_metadata = loads(response_data.get('error[metadata]'))

            razorpay_payment_id = error_metadata['payment_id']
            razorpay_order_id = error_metadata['order_id']

            try:
                transaction = Transaction.objects.get(razorpay_order_id=razorpay_order_id)
                transaction.status = 'failed'
                transaction.payment_timestamp = datetime.datetime.now()
                transaction.payment_id = razorpay_payment_id
                transaction.save()

                return render(request, 'error.html', {'err_msg': error_description})
            except:
                return JsonResponse({'message': 'Invalid order ID'})

        # Payment Success
        else:
            from django.utils import timezone
            from videos.utils import get_expiry_date

            razorpay_payment_id = response_data.get('razorpay_payment_id')
            razorpay_order_id = response_data.get('razorpay_order_id')
            razorpay_signature = response_data.get('razorpay_signature')
            try:
                transaction = Transaction.objects.get(razorpay_order_id=razorpay_order_id)
                transaction.status = 'paid'
                transaction.payment_timestamp = datetime.datetime.now()
                transaction.payment_id = razorpay_payment_id
                transaction.save()

                new_start_date = timezone.now()
                order = transaction.order
                order.status = 'completed'
                order.is_active = True
                order.start_date = new_start_date
                order.expiration_date = get_expiry_date(new_start_date, period=order.subscription_period)
                order.save()

                return render(request, 'success.html')
            except:
                return JsonResponse({'message': 'Invalid order ID'})
            # return Response({'message': response_data})


class PaymentCheckoutView(PaymentCheckoutTestView):
    def get_key_config(self):
        return live_config

    def get_order_id(self):
        order_id = self.request.POST.get('id', 10)
        if not order_id:
            order_id = self.request.GET.get('id', None)
        return order_id
