from django.urls import path

from accounts.views import login_view, logout_view, register_view, UserAdd
from accounts.profile import UserDetailView, UserList

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', register_view, name='create_acc'),
    path('add_user/<int:pk>/', UserAdd.as_view(), name='add_user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_profile'),
    path('users/', UserList.as_view(), name='user_list')
]