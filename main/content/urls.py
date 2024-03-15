from django.urls import path 
from .import views

urlpatterns = [
    path('home/',views.HomePageView.as_view(),name='home'),
    # Profile Page Paths
    path('profile/<int:pk>/',views.ProfileFreelancerView.as_view(),name='profile_freelancer'),
    path('profile/employer/<int:pk>/',views.ProfileEmployerView.as_view(),name='profile_employer'),
    # Edit Profile Paths
    path('edit/employer/<int:pk>/',views.EditProfileEmployerView.as_view(),name='edit_employer'),
    path('edit/freelancer/<int:pk>/',views.EditProfileFreelancerView.as_view(),name='edit_freelancer'),
    # Contact Us
    path('contact/',views.ContactUsView.as_view(),name='contact'),
    # Filter Project Paths
    path('projects/',views.ProjectsPageView.as_view(),name='projects'),
    path('filter/project/<slug:slug>/',views.FilterProjectView.as_view(),name='filter_project'),
    path('filter/freelancer/<slug:slug>/',views.FilterFreelancerView.as_view(),name='filter_freelancer'),
    # CRUD Project Paths
    path('create/project/',views.CreateProjectView.as_view(),name='create_project'),
    path('project/complete/',views.CreateCompleteProjectView.as_view(),name='project_complete'),
    path('list/projects/',views.ListProjectsView.as_view(),name='list_projects'),
    path('accept/project/<int:pk>/',views.AcceptProjectView.as_view(),name='accept_project'),
    path('reject/project/<int:pk>/',views.RejectProjectView.as_view(),name='reject_project'),
    path('delete/project/<int:pk>/',views.DeleteProjectView.as_view(),name='delete_project'),
    path('edit/project/<int:pk>/',views.EditProjectView.as_view(),name='edit_project'),
    path('detail/project/<slug:slug>/',views.DetailProjectView.as_view(),name='detail_project'), 
    path('freelancers/',views.ListFreelancersView.as_view(),name = 'list_freelancers'),
]
