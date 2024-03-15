from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import validate_integer

from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin

from .managers import UserManager

from ckeditor.fields import RichTextField
# Create your models here.

class Skill(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255 , null = True , blank=True)

    def __str__(self) -> str:
        return self.title


def validate_phone(value):
    if len(value) != 11:
        raise ValidationError('Number Phone invalid!')
    return value


class User(AbstractBaseUser , PermissionsMixin):

    STATUS = (
        ('Freelancer' , 'Freelancer'),
        ('Employer' , 'Employer'),
        
    )

    phone = models.CharField(max_length=11 ,validators=[validate_phone , validate_integer] , unique=True)
    username = models.CharField(max_length=50 , unique=True)
    email = models.EmailField(max_length=60,unique=True)
    status = models.CharField(max_length=10,choices=STATUS)
    skills = models.ManyToManyField(Skill , null=True , blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','username','status']

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
    
class OTP(models.Model):
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    created = models.DateTimeField(auto_now=True ,null=True , blank=True)

    def __str__(self) -> str:
        return f'{self.phone} Code Veryfy : {self.code}'
    
    
class City(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.title

# Profile Users
class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='userFreelancer' )
    city = models.ForeignKey(City , on_delete=models.CASCADE, null=True , blank=True)
    about = RichTextField(null=True , blank=True)
    cv = models.URLField(null=True , blank=True)
    image = models.ImageField(upload_to='profile/' , default='default_profile/default_profile_image.png')

    def __str__(self) -> str:
        return self.user.username
    
class UserEmployerProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='userEmployer')
    image = models.ImageField(upload_to='profile/' , default='default_profile/default_profile_image.png')

    def __str__(self) -> str:
        return self.user.username
    



    






