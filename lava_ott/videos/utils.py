from .models import Order
from django.utils import timezone


def get_expiry_date(date, period):
    from datetime import timedelta
    if period == 'month':
        days = 31
    elif period == 'year':
        days = 365.25
    else:
        days = 0

    exp_date = date + timedelta(days)
    print('Calculated Expiry date = ', date, '+', days, '=', exp_date)
    return exp_date


def get_order(order):
    return {
        "id": order.id,
        "user": order.user.get_full_name(),
        "subscription_amount": order.subscription_amount,
        "subscription_period": order.subscription_period,
        "status": order.status,
        "created_at": order.created_at.strftime("%d %m %Y"),
        "start_date": order.start_date.strftime("%d/%m/%Y") if order.start_date else '',
        "start_time": order.start_date.time().strftime("%H:%M%p") if order.start_date else '',
        "expiration_date": order.expiration_date.strftime("%d/%m/%Y") if order.expiration_date else '',
        "expiration_time": order.expiration_date.time().strftime("%H:%M%p") if order.expiration_date else '',
        "is_active": order.is_active,
    }


def get_orders(user):
    orders1 = Order.objects.filter(user=user, status='completed').order_by('-start_date')
    orders2 = Order.objects.filter(user=user).exclude(status='completed').order_by('-created_at')
    # orders = orders1.union(orders2).order_by('-start_date')
    orders = [get_order(order) for order in orders1] + [get_order(order) for order in orders2]

    return orders


def subscription_exists(user):
    from .models import Order
    from django.db.models import F

    orders = Order.objects.filter(user=user, status='completed')
    current_orders = orders.filter(start_date__lte=timezone.now(), expiration_date__gt=F('start_date'))
    later_orders = orders.filter(start_date__gte=timezone.now(), expiration_date__gt=F('start_date'))

    curr_order = None
    if current_orders.exists():
        curr_order = current_orders.earliest('start_date')

    elif later_orders.exists():
        curr_order = later_orders.earliest('start_date')

    if curr_order:
        curr_order.is_active = True
        curr_order.save()
        orders.exclude(id=curr_order.id).update(is_active=False)
        return True
    return False


def get_videos(video):
    return {
        "id": video.id,
        "name": video.name,
        "description": video.description,
        "thumbnail": video.thumbnail.url if video.thumbnail else '',
        "trailer": video.trailer.utl if video.trailer else '',
        "file": video.file.url if video.file else '',
        "director": video.director,
        "cast": video.cast,
        "watch_count": video.watch_count,
        "watch_hours": video.watch_hours
    }