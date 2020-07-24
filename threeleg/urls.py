from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('whoami', views.whoami, name='whoami'),
    path('courses', views.courses, name='courses'),
    path('users', views.users, name='users'),
    path('enrollments', views.enrollments, name='enrollments'),
    path('getusers', views.getusers, name='getusers'),
    path('get_auth_code', views.get_auth_code, name='get_auth_code'),
    path('get_access_token', views.get_access_token, name='get_access_token'),
    path('learnlogout', views.learnlogout, name='learnlogout')
]