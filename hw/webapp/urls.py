from django.urls import path

from webapp.views.task import (
    IndexView, 
    TaskView, 
    TaskCreate, 
    TaskEdit,
    TaskDelete
)
from webapp.views.project import (
    ProjectView, 
    ProjectDetail,
    ProjectCreate,
    ProjectUpdate, 
    ProjectDelete
)

urlpatterns = [
    path('', IndexView.as_view(), name='task_list'),
    path('task/<int:pk>', TaskView.as_view(), name='task_view'),
    path('project/<int:pk>/task/add', TaskCreate.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskEdit.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('project/', ProjectView.as_view(), name='project_view'),
    path('project/<int:pk>', ProjectDetail.as_view(), name='project_detail'),
    path('project/create/', ProjectCreate.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdate.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),
]