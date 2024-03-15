from django import template

from accounts.models import UserProfile

register = template.Library()


@register.inclusion_tag('accounts/inclusion_tags/profile_freelancer.html')
def profile_freelancer(pk):
    user = UserProfile.objects.get(user = pk)
    return {'user':user}