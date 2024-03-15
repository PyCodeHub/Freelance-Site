from django.utils import timezone
from django.core.mail import send_mail

from celery import shared_task

from .models import Project


@shared_task
def expire_projects_task():
    expire_project_time = timezone.now() - timezone.timedelta(days=30)
    Project.objects.filter(created__lt = expire_project_time).delete()
    return True


@shared_task
def contact_task(subject , message , email):
    send_mail(subject , message ,email , ['testpass935@gmail.com'] , fail_silently=False)
    print('Send Email...........')
    return True

