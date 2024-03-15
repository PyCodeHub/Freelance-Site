from django import template

from accounts.models import UserEmployerProfile

register = template.Library()


@register.inclusion_tag('accounts/inclusion_tags/profile_employer.html')
def profile_employer(pk):
    user = UserEmployerProfile.objects.get(user = pk)
    return {'user':user}
