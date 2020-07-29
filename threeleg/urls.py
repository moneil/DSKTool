from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('isup', views.isup, name='isup'),
    path('whoami', views.whoami, name='whoami'),
    path('courses', views.courses, name='courses'),
    path('users', views.users, name='users'),
    path('enrollments', views.enrollments, name='enrollments'),
    path('get_auth_code', views.get_auth_code, name='get_auth_code'),
    path('get_access_token', views.get_access_token, name='get_access_token'),
    path('learnlogout', views.learnlogout, name='learnlogout'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('notauthorized', views.notauthorized, name='notauthorized')
]