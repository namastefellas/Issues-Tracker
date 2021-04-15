from django.urls import path

from accounts.views import login_view, logout_view, register_view, UserAdd

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', register_view, name='create_acc'),
    path('add_user/<int:pk>/', UserAdd.as_view(), name='add_user')
]