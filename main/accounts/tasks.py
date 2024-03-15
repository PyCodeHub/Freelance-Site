from celery import shared_task

from django.utils import timezone

from .models import OTP


@shared_task
def expire_otps_task():
    expire_time = timezone.now() - timezone.timedelta(minutes=1)
    OTP.objects.filter(created__lt = expire_time).delete()
    return True