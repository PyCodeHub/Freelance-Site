from django.urls import path 
from .import views

urlpatterns = [
    # User Register Paths 
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('veryfy/',views.UserVeryfyCodeView.as_view(),name='veryfy'),
    path('employer/form/',views.EmployerRegisterView.as_view(),name='employer'),
    path('freelancer/form/',views.FreelancerRegisterView.as_view(),name = 'freelancer'),
    # UserLogin Paths
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('login/veryfy/',views.LoginVeryfyCodeView.as_view(),name='login_veryfy'),
    # Logout
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    # Reset Password Paths
    path('password/reset/form/',views.UserPasswordResetView.as_view(),name='password_reset_form'),
    path('password/reset/done/',views.UserPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/',views.UserPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
]
