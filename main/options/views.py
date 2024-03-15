from django.http.response import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.mail import send_mail
from accounts.models import UserProfile
from content.models import Project

from .models import *
from .forms import ReplyCommentForm , UpdateCommentForm , RecruitmentForm

from accounts.models import User

# Save freelancer's favorite projects
class SaveProjectView(View):
    def get(self ,request , pk):
        project = Project.objects.get(id = pk)
        check = SaveProject.objects.filter(project = project)
        if check.exists():
            check.delete()
            return redirect('home')
        else:
            SaveProject.objects.create(user = request.user , project = project)
            return redirect('home')


class ListProjectSaveView(View):
    template_name = 'options/listProjectSaves.html'

    def get(self , request):
        user = request.user
        saves = user.saves.all()
        #saves = SaveProject.objects.filter(user = request.user)
        return render(request,self.template_name,{'saves':saves})


# Reply Comment Employer
class ReplyCommentView(View):
    template_name = 'options/replyComments.html'
    form_class = ReplyCommentForm

    def setup(self, request, *args, **kwargs) :
        self.comment_instance = Comment.objects.get(id = kwargs['comment_id'])
        return super().setup(request, *args, **kwargs)

    def get(self , request , profile_id , comment_id):
        comment = self.comment_instance
        return render(request,self.template_name,{
            'form':self.form_class,
            'comment':comment,
        })
    
    def post(self , request , profile_id , comment_id):
        comment = self.comment_instance
        profile_freelancer = UserProfile.objects.get(user = profile_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            if request.user.status == 'Freelancer':
                comment_reply = form.save(commit=False)
                comment_reply.user = request.user
                comment_reply.freelancer = profile_freelancer
                comment_reply.reply = comment
                comment_reply.is_reply = True
                comment_reply.save()
                return redirect('home')
            return redirect('home')
        return render(request,self.template_name,{'form':form})

# Delete and Edit Comment Employer
class DeleteCommentView(View):

    def get(self , request , pk):
        comment = Comment.objects.get(id = pk)
        if comment.user.id == request.user.id :
            comment.delete()
            return redirect('home')
        else:
            return redirect('home')
        
        
class UpdateCommentView(View):
    template_name = 'options/updateComment.html'
    form_class = UpdateCommentForm

    def setup(self, request, *args, **kwargs) :
        self.comment_instance = Comment.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        comment = self.comment_instance
        if not comment.user.id == request.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)    
    
    def get(self , request , pk):
        comment = self.comment_instance
        form = self.form_class(instance=comment)
        return render(request,self.template_name,{'form':form})
    
    def post(self , request , pk):
        comment = self.comment_instance
        form = self.form_class(request.POST , instance=comment)

        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request,self.template_name,{'form':form})
    
    
# Requests from freelancers to receive projects
class RequestFreelancerView(LoginRequiredMixin,View):

    def get(self , request , project_id):
        project = Project.objects.get(id = project_id)

        if request.user.status == 'Freelancer':
            check = RequestFreelancer.objects.filter(user = request.user , project = project)
            if check.exists():
                return redirect('home')
            else:
                RequestFreelancer.objects.create(
                user = request.user,
                project = project
            )
                msg = 'Hello {0} Freelancer {1} Request Project {2} \n http://127.0.0.1:8000/content/home/'.format(
                    project.user.username,
                    request.user.username,
                    project.title
                ) 
                send_mail('',msg,'testpass935@gmail.com',[project.user.email],fail_silently=False)
            return redirect('complete_request_freelancer')       
        return redirect('home')
    
class CompleteRequestFreelancer(View):
    template_name = 'options/completeRequestFreelancer.html'

    def get(self , request):
        return render(request,self.template_name)


class ListRequestFreelancer(LoginRequiredMixin,View):
    template_name ='options/listRequestFreelancer.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated :
            if request.user.status == 'Employer':
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request): 
        user = request.user
        requests = user.userRequest.filter(is_accept = False)
        employment = RequestEmployer.objects.filter(freelancer__user = user , is_accept = False)
        return render(request,self.template_name,{
            'requests':requests,
            'employment':employment,
        })
    
class CanselRequestFreelancerView(LoginRequiredMixin,View):

    def dispatch(self, request, *args, **kwargs) :

        if request.user.is_authenticated :
            get_request = RequestFreelancer.objects.get(id = kwargs['pk'])
            if not get_request.user.id == request.user.id :
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request , pk):
        get_request = RequestFreelancer.objects.get(id = pk)
        get_request.delete()
        return redirect('home')
    
class ListRequestEmployer(LoginRequiredMixin,View):
    template_name ='options/listRequestEmployer.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated :
            if request.user.status == 'Freelancer':
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request): 
        user = request.user
        requests = RequestFreelancer.objects.filter(project__user = user )
        employments = user.requestEmployer.filter(is_accept = False)
        return render(request,self.template_name,{
            'requests':requests,
            'employments':employments,
        })


class RejectRequestFreelancerView(LoginRequiredMixin,View):

    def setup(self, request, *args, **kwargs) :
        self.get_request_instance = RequestFreelancer.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        get_request = self.get_request_instance
        if request.user.is_authenticated :
            if not get_request.project.user.id == request.user.id:
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        get_request = self.get_request_instance
        get_request.delete()

        msg = "Sorry Employer {0} rejected your request to do the project {1}".format(
            get_request.project.user.username,
            get_request.project.title
        )
        send_mail("",msg , 'testpass935@gmail.com' , [get_request.user.email] , fail_silently=False)

        return redirect('home')
    
class AcceptRequestFreelancerView(View):

    def setup(self, request, *args, **kwargs) -> None:
        self.get_request_instance = RequestFreelancer.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        get_request = self.get_request_instance
        if request.user.is_authenticated :
            if not get_request.project.user.id == request.user.id:
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        get_request = self.get_request_instance
        get_request.is_accept = True
        get_request.project.complete = True

        get_request.project.save()
        get_request.save()

        msg = """
            Hello {0} Employer {1} accept your request to do the project {2} \n
            ways to communicate with the employer {3} \n
            Phone : {4} \n
            Email : {5}
        """.format(
            get_request.user.username,
            get_request.project.user.username,
            get_request.project.title,
            get_request.project.user.username,
            get_request.project.user.phone,
            get_request.project.user.email,
        )

        send_mail("",msg , 'testpass935@gmail.com' , [get_request.user.email] , fail_silently=False)
        return redirect('home')
    

class RecruitmentView(LoginRequiredMixin,View):
    template_name = 'options/recruitmentForm.html'
    form_class = RecruitmentForm

    def setup(self, request, *args, **kwargs) :
        self.freelancer_instance = UserProfile.objects.get(user = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            if request.user.status == 'Freelancer':
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        freelancer = self.freelancer_instance
        projects = Project.objects.filter(user = request.user)
        return render(request,self.template_name,{
            'form':self.form_class,
            'freelancer':freelancer,
            'projects':projects,

        })

    def post(self , request , pk):
        freelancer = self.freelancer_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            selected_project_id = request.POST.get('project')
            get_project = Project.objects.get(id = selected_project_id)
            check = RequestEmployer.objects.filter(
                freelancer = freelancer,
                employer = request.user,
                project = get_project
            )

            if check.exists():
                return redirect('home')
            
            else:
                RequestEmployer.objects.create(
                    employer = request.user,
                    freelancer = freelancer,
                    project = get_project,
                    content = cd['content']
                )
                return redirect('home')
        return render(request,self.template_name,{'form':form})
    

class RejectRecruitmentView(LoginRequiredMixin,View):

    def setup(self, request, *args, **kwargs):
        self.employment_instance = RequestEmployer.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        employment = self.employment_instance

        if not employment.freelancer.user.id == request.user.id:
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        employment = self.employment_instance
        employment.delete()
        return redirect('home')
    
class AcceptRecruitmentView(LoginRequiredMixin,View):

    def setup(self, request, *args, **kwargs):
        self.employment_instance = RequestEmployer.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        employment = self.employment_instance

        if not employment.freelancer.user.id == request.user.id:
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        employment = self.employment_instance
        employment.is_accept = True
        employment.project.complete = True

        employment.project.save()
        employment.save()

        return redirect('home')
    

class CancelRecruitmentView(LoginRequiredMixin,View):

    def setup(self, request, *args , **kwargs) :
        self.recruitment_instance = RequestEmployer.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        recruitment = self.recruitment_instance

        if not recruitment.employer.id == request.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request , *args , **kwargs):
        recruitment = self.recruitment_instance
        recruitment.delete()
        return redirect('home')

    

    


    

    

