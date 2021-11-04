from django.urls import path
from .views import *
from . import views

app_name = 'account'
urlpatterns = [

    path('', IndexView.as_view(), name='main_url'),  # main page
    path('register/', UserRegister.as_view(), name='signup_url'),  # sing up
    path('login/', views.user_login, name='login_url'),  # login
    path('logout/', views.user_logout, name='logout_url'),  # logout
    path('permissions/', Perms.as_view(), name='permission_url'),  # logout
    path('change_perms/', views.change_perms, name='change_perm'),  # permission page

    path('api/', UserList.as_view()),  # Users list API
    path('api/<int:pk>/', UserDetail.as_view()),  # User detail API

]
