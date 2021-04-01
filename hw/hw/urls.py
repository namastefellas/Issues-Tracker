"""hw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views.task import IndexView, TaskView, TaskCreate, TaskEdit, TaskDelete
from webapp.views.project import ProjectView, ProjectDetail, ProjectCreate, ProjectUpdate, ProjectDelete



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='task_list'),
    path('task/<int:pk>', TaskView.as_view(), name='task_view'),
    path('project/<int:pk>/task/add', TaskCreate.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskEdit.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('project/', ProjectView.as_view(), name='project_view'),
    path('project/<int:pk>', ProjectDetail.as_view(), name='project_detail'),
    path('project/create/', ProjectCreate.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdate.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete')
]
