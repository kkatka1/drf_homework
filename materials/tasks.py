import logging
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def subscription_message(course, email):
    send_mail(
        subject="Сообщение о подписке",
        message=f"Материалы курса {course} обновились",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
