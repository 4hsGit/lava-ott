# ----------------- API for Mobile App ---------------------- #

from rest_framework.response import Response
from django.utils import timezone
from ..models import Video, Order
from ..serializers import (
    VideoListSerializer,
    OrderCreateSerializer,
    OrderListSerializer
)
from ..utils import get_order
from users.utils import get_paginated_list, format_errors
from users.custom_views import CustomAuthenticateAppView


class VideoListAppView(CustomAuthenticateAppView):
    def get_response(self, request, user):
        post = request.data.get
        page = post('page', 1)
        per_page = post('per_page', 10)

        videos = Video.objects.filter(view_on_app=True)
        data = get_paginated_list(videos, page, per_page)
        serializer = VideoListSerializer(data['data'], many=True)
        data['data'] = serializer.data

        return Response({'status': True, 'data': data})


class OrderCreateView(CustomAuthenticateAppView):
    def get_response(self, request, user):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'status': True, 'message': 'Order created', 'data': serializer.data})
        else:
            return Response({'status': False, 'error': format_errors(serializer.errors)})


class OrderListView(CustomAuthenticateAppView):
    def get_response(self, request, user):
        from ..utils import get_orders
        # serializer = OrderListSerializer(orders, many=True)
        return Response({'status': True, 'data': get_orders(user)})


class CheckSubscriptionView(CustomAuthenticateAppView):
    def get_response(self, request, user):
        is_subscribed = user.has_subscription()
        data = {
            'status': True,
            'is_subscribed': is_subscribed
        }
        if is_subscribed is True:
            # serializer = OrderListSerializer(orders, many=True)
            data.update({'order': get_order(user.get_active_subscription())})

        return Response(data)


class SubscriptionView(CustomAuthenticateAppView):

    def get_response(self, request, user):
        from ..utils import get_expiry_date
        order_id = request.data.get('id')

        is_subscribed = user.has_subscription()
        new_start_date = timezone.now()
        if is_subscribed is True:
            from datetime import timedelta
            order = user.get_active_subscription()
            start_date = order.start_date
            print('Stat date of active order = ', start_date)
            new_start_date = start_date + timedelta(seconds=1)
            # return Response({'status': False, 'message': 'Subscription already exist.'})
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'completed'
            order.is_active = True
            order.start_date = new_start_date
            order.expiration_date = get_expiry_date(new_start_date, period=order.subscription_period)
            order.save()

            return Response({'status': True, 'message': 'Subscription added.'})
        except Order.DoesNotExist:
            return Response({'status': False, 'message': 'Order ID does not exist.'})
        except Exception as e:
            return Response({'status': False, 'message': f'Error - {str(e)}'})


class VideoPlayView(CustomAuthenticateAppView):
    def get_response(self, request, user):
        video_id = request.data.get('video')

        is_subscribed = user.has_subscription()
        if user.has_subscription() is True:
            from ..utils import get_videos
            try:
                video = Video.objects.get(id=video_id)
                return Response({'status': True, 'data': get_videos(video)})
            except Video.DoesNotExist:
                return Response({
                    'status': False,
                    'is_subscribed': is_subscribed,
                    'message': 'Video ID does not exist.'
                })
        else:
            return Response({
                'status': True,
                'is_subscribed': is_subscribed
            })
