from django.db import models
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from json import loads


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('T', 'Transgender'), ('O', 'Others')]

    mobile_number = models.CharField(max_length=25, unique=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)

    is_subscriber = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)

    keep_me_loggedin = models.BooleanField(default=False)

    def has_subscription(self):
        from videos.utils import subscription_exists
        return subscription_exists(self)

    def get_active_subscription(self):
        from videos.utils import get_order
        from videos.models import Order
        from django.core.exceptions import MultipleObjectsReturned
        try:
            order = Order.objects.get(user=self, status='completed', is_active=True, expiration_date__gt=timezone.now())
            order = get_order(order)
        except Order.DoesNotExist:
            order = {}
        except Order.MultipleObjectsReturned:
            raise MultipleObjectsReturned

        return order

    def get_session_age(self):
        if self.is_admin is True:
            return settings.ADMIN_SESSION_AGE
        else:
            if self.keep_me_loggedin is True:
                return 3600 * 24 * 14
        return 3600 * 24


class CustomSession(models.Model):
    session_key = models.TextField(primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    @classmethod
    def generate_session_key(cls):
        key = Fernet.generate_key()
        if cls.objects.filter(session_key=key.decode()).exists():
            cls.generate_session_key()
        return key

    @classmethod
    def set_session(cls, user, payload=None):
        key = cls.generate_session_key()
        f = Fernet(key)
        if payload is None:
            data = {'user_id': user.id}
        else:
            data = payload
        session_data = f.encrypt(str(data).encode()).decode()
        key = key.decode()

        expiry = timezone.now() + get_expiry(user)

        cls(session_key=key, session_data=session_data, expire_date=expiry).save()
        return key

    @classmethod
    def get_session(cls, token):
        try:
            obj = cls.objects.get(session_key=token)

            if session_expired(obj):
                return False

            session_data = obj.session_data.encode()
            f = Fernet(token.encode())
            data = f.decrypt(session_data).decode()
            data = str_to_json(data)
            print('Data: ', data)

            user = User.objects.get(id=data['user_id'])

            obj.expire_date = timezone.now() + get_expiry(user)
            obj.save()
            obj.refresh_from_db()

            print('Current Exp date: ', obj.expire_date)

            return user
        except User.DoesNotExist:
            print('No user exists. or invalid token...')
        except Exception as e:
            print('Error: ', str(e))
        return False

    @classmethod
    def delete_session(cls, token):
        print('----------------------------')
        try:
            obj = CustomSession.objects.get(session_key=token)

            print('---kjhkj-------------------------', obj)
            cls.objects.get(session_key=token).delete()
        except:
            print('Nooooo')
            pass

    @classmethod
    def delete_expired_sessions(cls):
        today = timezone.now() - timedelta(days=1)
        cls.objects.filter(expire_date__lte=today).delete()


def str_to_json(data):
    data = data.replace("'", '"')
    return loads(data)


def session_expired(obj):
    expire_date = obj.expire_date
    current_time = timezone.now()

    print(expire_date, current_time)

    if expire_date < current_time:
        return True


def get_expiry(user):
    expiry = timedelta(seconds=user.get_session_age())
    # expiry = timezone.now() + timedelta(seconds=30)
    print('session_age: ', user.get_session_age())
    return expiry