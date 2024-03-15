from django.db.models.signals import post_save
from .models import User , UserEmployerProfile , UserProfile


def create_profile(sender , **kwargs):
    if kwargs['created']:
        if kwargs['instance'].status == 'Freelancer':
            UserProfile.objects.create(
                user = kwargs['instance']
            )
        else:
            UserEmployerProfile.objects.create(
                user = kwargs['instance']
            )

post_save.connect(receiver=create_profile , sender=User)