# urls.py
from django.urls import path
from .views import UserListView, UserCreateView, UserLoginView

urlpatterns = [
    path('get-users/', UserListView.as_view(), name='user_list'),
    path('new-user/', UserCreateView.as_view(), name='create_user'),
    path('login-user/', UserLoginView.as_view(), name='login_user'),
]
