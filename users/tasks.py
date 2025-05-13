from dateutil.relativedelta import relativedelta
from django.utils import timezone
from celery import shared_task
from users.models import User


@shared_task
def block_user():
    month_ago = timezone.now() - relativedelta(months=1)
    users = User.objects.filter(last_login__lte=month_ago, is_active=True)
    users.update(is_active=False)