from django.db import models

from accounts.models import User , Skill
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60 , null=True , blank=True)

    def __str__(self) -> str:
        return self.title

class Project(models.Model):

    STATUS = [
        ('Accept','Accept'),
        ('Checking','Checking'),
        ('Reject','Reject'),
    ]

    user = models.ForeignKey(User , on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60 , null=True , blank=True)
    category = models.ManyToManyField(Category)
    skills = models.ManyToManyField(Skill)
    time = models.SmallIntegerField()
    content = models.TextField(max_length=100)
    price = models.IntegerField()
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS, default='Checking')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    def user_can_save(self , user):
        check = user.saves.filter(project = self )
        if check.exists():
            return True
        return False

    

