from django.shortcuts import render , redirect
from django.views import View
from django.core.mail import send_mail
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator

import random

from accounts.models import UserProfile , UserEmployerProfile , User , Skill
from accounts.forms import (
    EditAccountEmployerForm,
    EditAccountFreelancerForm,
    EditProfileEmployerForm,
    EditProfileFreelancerForm
)


from options.forms import AddCommentForm
from options.models import Comment 

from .forms import ContactUsForm ,CreateProjectForm , EditProjectForm
from .models import Project , Category

from .tasks import contact_task

# Create your views here.



class HomePageView(View):
    template_name = 'content/homePage.html'

    def get(self , request):
        categorys = Category.objects.all()
        skills = Skill.objects.all()
        return render(request,self.template_name,{
            'categorys':categorys,
            'skills':skills,
        })


# Users Profile Page
class ProfileFreelancerView(View):
    template_name = 'content/profileFreelancer.html'
    form_class = AddCommentForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = UserProfile.objects.get(user = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        user = self.user_instance
        if request.user.is_authenticated:
            if request.user.status == 'Freelancer':
                if not user.user.id == request.user.id:
                    return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        user = self.user_instance
        comments = user.freelancerComment.filter(is_reply = False)
        return render(request,self.template_name,{
            'user':user,
            'form':self.form_class, 
            'comments':comments,
        })
    
    @method_decorator(login_required)
    def post(self , request , pk):
        user = request.user
        freelancer = self.user_instance
        form = self.form_class(request.POST)

        if form.is_valid():
            if request.user.status == 'Employer':
                new_comment = form.save(commit=False)
                new_comment.user = user
                new_comment.freelancer = freelancer
                new_comment.save()
                return redirect('home')
            return redirect('home')
        return render(request,self.template_name,{'form':form})

class ProfileEmployerView(View):
    template_name = 'content/profileEmployer.html'

    def dispatch(self, request, *args, **kwargs) :
        user = UserEmployerProfile.objects.get(user = kwargs['pk'] )
        if not request.user.id == user.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        user = UserEmployerProfile.objects.get(user = pk)
        #projects = Project.objects.filter(user = pk , status = 'Accept')

        projects = user.user.posts.filter(status = 'Accept')
        return render(request,self.template_name,{
            'user':user,
            'projects':projects
        })

# Edit Profile Users Views
class EditProfileEmployerView(LoginRequiredMixin,View):
    template_name = 'content/editEmployer.html'
    form_profile = EditProfileEmployerForm
    form_account = EditAccountEmployerForm

    def dispatch(self, request, *args, **kwargs):
        user = UserEmployerProfile.objects.get(user = kwargs['pk'])
        if not request.user.id == user.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self ,request , pk):
        user = UserEmployerProfile.objects.get(user = pk)
        user_ins = User.objects.get(id = pk)

        form_profile = self.form_profile(instance=user)
        form_account = self.form_account(instance=user_ins)

        return render(request,self.template_name,{
            'form_profile':form_profile , 
            'form_account':form_account ,
        })

    def post(self ,request , pk):
        user = UserEmployerProfile.objects.get(user = pk)
        user_ins = User.objects.get(id = pk)

        form_profile = self.form_profile(request.POST , request.FILES , instance=user)
        form_account = self.form_account(request.POST , instance=user_ins)

        if form_profile.is_valid() and form_account.is_valid():
            form_profile.save()
            form_account.save()
            return redirect('home')
        
        return render(request,self.template_name,{
            'form_profile':form_profile,
            'form_account':form_account
        })
    
class EditProfileFreelancerView(LoginRequiredMixin,View):
    template_name = 'content/editFreelancer.html'
    form_profile = EditProfileFreelancerForm
    form_account = EditAccountFreelancerForm

    def setup(self, request, *args, **kwargs) :
        self.userProfile_instance = UserProfile.objects.get(user = kwargs['pk'])
        self.user_instance = User.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        user = self.userProfile_instance
        if not request.user.id == user.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self ,request , pk):
        user = self.userProfile_instance
        user_ins = self.user_instance

        form_profile = self.form_profile(instance=user)
        form_account = self.form_account(instance=user_ins)

        return render(request,self.template_name,{
            'form_profile':form_profile,
            'form_account':form_account,
        })
    
    def post(self , request, pk):
        user = self.userProfile_instance
        user_ins = self.user_instance

        form_profile = self.form_profile(request.POST, request.FILES , instance=user)
        form_account = self.form_account(request.POST , instance=user_ins)

        if form_profile.is_valid() and form_account.is_valid():
            form_profile.save()
            form_account.save()
            return redirect('home')
        
        return render(request,self.template_name,{
            'form_profile':form_profile,
            'form_account':form_account,
        })
    
    
# Contact Us Page View
class ContactUsView(View):
    template_name = 'content/contact.html'
    form_class = ContactUsForm

    def get(self , request):
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self ,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            msg = 'Phone : {0} \n Email : {1} \n Subject : {2} \n Message : {3}'.format(
                cd['phone'],
                cd['email'],
                cd['subject'],
                cd['message'],
            )
            send_mail(cd['subject'] ,msg , cd['email'] ,['testpass935@gmail.com'] , fail_silently=False)
            #contact_task.delay(cd['subject'] , msg , cd['email'])
            
            return redirect('home')
        return render(request,self.template_name,{'form':form})


# Views related to projects
class ProjectsPageView(View):
    template_name = 'content/projectsPage.html'

    def get(self , request):
        projects = Project.objects.filter(status = 'Accept' , complete = False)
        return render(request,self.template_name,{'projects':projects})
    

class FilterProjectView(View):
    template_name = 'content/filterProject.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.status == 'Employer':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request , slug):
        category = Category.objects.get(slug = slug)
        projects = Project.objects.filter(category = category , status = 'Accept')
        return render(request,self.template_name,{'projects':projects})
    
class FilterFreelancerView(View):
    template_name = 'content/filterFreelancer.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.status == 'Freelancer':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request , slug):
        skill = Skill.objects.get(slug = slug)
        freelancers = User.objects.filter(skills = skill)
        return render(request,self.template_name,{'freelancers':freelancers})

# CRUD Projects
class CreateProjectView(LoginRequiredMixin,View):
    #permission_required = 'content.add_project'
    template_name = 'content/createProject.html'
    form_class = CreateProjectForm


    def dispatch(self, request , *args, **kwargs ) :
        if request.user.is_authenticated:
            if request.user.status == 'Freelancer':
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self ,request):
        return render(request,self.template_name , {'form':self.form_class})
    
    def post(self ,request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            if request.user.status == 'Employer':
                cd = form.cleaned_data
                new_project = Project.objects.create(
                    user = request.user,
                    title = cd['title'], 
                    slug =  slugify(cd['title']),
                    content = cd['content'],
                    time = cd['time'],
                    price = cd['price'],
                )
                new_project.category.set(cd['category'])
                new_project.skills.set(cd['skills'])
                return redirect('project_complete')
            else:
                return redirect('home')
        return render(request,self.template_name,{'form':form})

class CreateCompleteProjectView(View):
    template_name = 'content/createCompleteProject.html'

    def get(self , request):
        return render(request,self.template_name)
    
class ListProjectsView(View):
    template_name = 'content/listProjects.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        projects = Project.objects.filter(status = 'Checking')
        return render(request,self.template_name,{'projects':projects})

# Edit Condition Projects
class AcceptProjectView(View):
    def get(self , request , pk):
        project = Project.objects.get(id = pk)
        project.status = 'Accept'
        project.save()

        msg = 'Hello {0} your project has been successfuly registered the site'.format(project.user.username)
        send_mail(
            msg,
            msg,
            'testpass935@gmail.com',
            [f'{project.user.email}']
        )
        return redirect('home')
    
class RejectProjectView(View):
    def get(self , request , pk):
        project = Project.objects.get(id = pk)
        project.delete()
        
        msg = 'Hello {0} your project was not registered the site'.format(project.user.username)
        send_mail(
            msg,
            msg,
            'testpass935@gmail.com',
            [f'{project.user.email}']
        )
        return redirect('home')
    

class DeleteProjectView(View):

    def dispatch(self, request, *args, **kwargs) :
        project = Project.objects.get(id = kwargs['pk'])
        if not project.user.id == request.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self ,request , pk):
        project = Project.objects.get(id = pk)
        project.delete()
        return redirect('home')

    
class EditProjectView(LoginRequiredMixin,View):
    template_name = 'content/editProject.html'
    form_class = EditProjectForm

    def setup(self, request, *args, **kwargs) :
        self.project_instance = Project.objects.get(id = kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs) :
        project = self.project_instance
        if not project.user.id == request.user.id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request , pk):
        project = self.project_instance
        form = self.form_class(instance=project)
        return render(request,self.template_name,{'form':form})
    
    def post(self , request , pk):
        project = self.project_instance
        form = self.form_class(request.POST , instance=project)

        if form.is_valid():
            cd = form.cleaned_data
            edit_project = form.save(commit=False)
            edit_project.slug = slugify(cd['title'])
            edit_project.status = 'Checking'
            edit_project.save()

            return redirect('home')
        return render(request,self.template_name,{'form':form})

class DetailProjectView(View):
    template_name = 'content/detailProject.html'

    def get(self , request , slug):
        project = Project.objects.get(slug = slug)
        is_save = False

        #check = SaveProject.objects.filter(user = request.user , project = project)
        #if check.exists():
        #    is_save = True

        if request.user.is_authenticated and project.user_can_save(request.user):
            is_save = True

        # Suggestion Project
        projects = Project.objects.filter(status = 'Accept')
        suggestion_projects = random.sample(list(projects),k=2)
   
        return render(request,self.template_name,{
            'project':project,
            'suggestion_projects':suggestion_projects,
            'is_save':is_save,
        })
    
class ListFreelancersView(View):
    template_name = 'content/freelancersList.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.status == 'Freelancer':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        freelancers = UserProfile.objects.all()
        return render(request,self.template_name,{'freelancers':freelancers})
    

    

    

    

    

    


