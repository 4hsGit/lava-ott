from django.core.paginator import Paginator, EmptyPage
from cryptography.fernet import Fernet
from rest_framework.response import Response
from django.utils import timezone


def format_errors(err):
    return {i: j[0] for i, j in err.items()}


def add_success_response(data, status=200):
    response = {
        'status': 'success'
    }
    response.update(data)
    return Response(response, status=status)


def add_error_response(data, status=500):
    response = {
        'status': 'success'
    }
    response.update(data)
    return Response(response, status=status)


def get_paginated_list(data, page=1, per_page=10):
    paginator = Paginator(data, per_page)
    num_pages = paginator.num_pages
    page_obj = paginator.page(page)

    if page_obj.has_next():
        next_page = page_obj.next_page_number()
    else:
        next_page = ''
    if page_obj.has_previous():
        previous_page = page_obj.previous_page_number()
    else:
        previous_page = ''

    data = page_obj.object_list

    return {
        "status": 'success',
        "page": page,
        "total_pages": num_pages,
        "next_page": next_page,
        "previous_page": previous_page,
        "total_count": paginator.count,
        "count": len(data),
        "data": data
    }


def get_key():
    from django.conf import settings
    from pathlib import Path
    import os

    file_path = os.path.join(settings.BASE_DIR, 'token-key.txt')
    print('file_path = ', file_path)
    file_path = Path(file_path)
    if file_path.exists():
        f = open(file_path, 'rb')
        key = f.read()
        return key
    # else:
    #     with open(file_path, 'wb') as f:
    #         f.write(Fernet.generate_key())
    #         get_key()
    return False


def generate_token(user):

    mobile_number = user.mobile_number
    user_id = user.id

    data = f'la{mobile_number}::ot{user_id}'
    print('-------- data ---- ', data)
    key = get_key()
    print('key = ', key)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()


def decode_token(token):
    key = get_key()
    decrypted_data = Fernet(key).decrypt(token).decode()
    print('decrypted data = ', decrypted_data)
    decrypted_data = decrypted_data.split('::')
    user_mob = decrypted_data[0].replace('la', '')
    user_id = decrypted_data[1].replace('ot', '')

    try:
        user_mob, user_id = user_mob.strip(), user_id.strip()
        print(user_mob, user_id)
        return [user_mob, user_id]
    except Exception as e:
        print('Error', str(e))
        return False


def authenticate_token(token):
    if not token:
        return False
    auth_status = decode_token(token)
    print('Decode response = ', auth_status)
    if auth_status is False:
        return False
    else:
        from .models import User
        try:
            user = User.objects.get(username=auth_status[0], id=auth_status[1])

            today = timezone.now()
            if user.session_expire_date:
                if user.session_expire_date < today:
                    return False

            if user.session_key != token:
                return False

            return user

        except User.DoesNotExist:
            print('except User.DoesNotExist:')
            return False


def get_masked_number(user):
    mobile_number = user.mobile_number
    if mobile_number:
        l = len(mobile_number)
        n = l//3
        mobile_number = str(mobile_number)[:n] + '***' + str(mobile_number)[-(int(n)):]
        return mobile_number
    return ''
