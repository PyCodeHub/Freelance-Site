from django.db import models

from accounts.models import User  , UserProfile , UserEmployerProfile

from content.models import Project
# Create your models here.


class SaveProject(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='saves')
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Save Project {self.project.title}'
    

class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='userComment')
    freelancer = models.ForeignKey(UserProfile , on_delete=models.CASCADE , related_name='freelancerComment')
    reply = models.ForeignKey('Comment' , on_delete=models.CASCADE , related_name='replyComment' , null=True , blank=True)
    is_reply = models.BooleanField(default=False)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Commented : {self.content[:15]}'


class RequestFreelancer(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE,related_name='userRequest')
    project = models.ForeignKey(Project , on_delete=models.CASCADE,related_name='projectRequest')
    is_accept = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Request {self.project.title}'


class RequestEmployer(models.Model):
    employer = models.ForeignKey(User , on_delete=models.CASCADE , related_name='requestEmployer')
    freelancer = models.ForeignKey(UserProfile , on_delete=models.CASCADE , related_name='freelancerRequest')
    project = models.ForeignKey(Project , on_delete=models.CASCADE)
    content = models.TextField()
    is_accept = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.employer.username} Request {self.freelancer.user.username}'
    
    
    
    

    

    
    
    
