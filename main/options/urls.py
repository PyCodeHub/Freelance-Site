from django.urls import path 
from .import views

urlpatterns = [
    # Save freelancer's favorite projects
    path('save/<int:pk>/',views.SaveProjectView.as_view(),name='save_project'),
    path('saves/',views.ListProjectSaveView.as_view(),name='list_save'),

    # CRUD Comment Paths
    path('reply/<int:profile_id>/<int:comment_id>/',views.ReplyCommentView.as_view(),name = 'reply'),
    path('delete/comment/<int:pk>/',views.DeleteCommentView.as_view(),name='delete_comment'),
    path('update/comment/<int:pk>/',views.UpdateCommentView.as_view(),name='update_comment'),

    # Requests from freelancers to receive projects
    path('request/freelancer/<int:project_id>/',views.RequestFreelancerView.as_view(),name='request_freelancer'),
    path('complete/request/freelancer/',views.CompleteRequestFreelancer.as_view(),name='complete_request_freelancer'),
    path('request/freelancer/',views.ListRequestFreelancer.as_view(),name='list_request_freelancer'),
    path('cancel/request/<int:pk>/',views.CanselRequestFreelancerView.as_view(),name='cancel_request'),
    path('request/employer/',views.ListRequestEmployer.as_view(),name='list_request_employer'),

    path('reject/request/<int:pk>/',views.RejectRequestFreelancerView.as_view(),name='reject_request'),
    path('accept/request/<int:pk>/',views.AcceptRequestFreelancerView.as_view(),name='accept_request'),

    path('recruitment/<int:pk>/',views.RecruitmentView.as_view(),name='recruitment'),

    path('reject/recruitment/<int:pk>/',views.RejectRecruitmentView.as_view(),name='reject_recruitment'),
    path('accept/recruitment/<int:pk>/',views.AcceptRecruitmentView.as_view(),name='accept_recruitment'),
    path('cancel/recruitment/<int:pk>/',views.CancelRecruitmentView.as_view(),name='cancel_recruitment'),
]
