from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Task, Project
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


from webapp.forms import TaskForm, SearchForm
# from webapp.base_view import CustomFormView



# Create your views here.

class IndexView(ListView):
    template_name = 'task/index.html'
    model = Task
    context_object_name = 'tasks'
    ordering = ('summary', '-created_at')
    paginate_by = 3
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_data) |
                Q(description__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context


class TaskView(DetailView):
    template_name = 'task/task_view.html'
    model = Task


class TaskCreate(PermissionRequiredMixin, CreateView):
    template_name = 'task/task_create.html' 
    model = Task
    form_class = TaskForm
    permission_required = 'webapp.task_create'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('webapp:project_detail', pk=self.kwargs.get('pk'))

    def has_permission(self):
        project = self.get_object_or_404()
        return super().has_permission() and self.request.user in project.user.all()
    

class TaskEdit(PermissionRequiredMixin, UpdateView):
    form_class = TaskForm
    model = Task
    template_name = 'task/task_edit.html'
    context_object_name = 'task'
    permission_required = 'webapp.task_edit'

    def has_permission(self):
        task = self.get_object()
        return super().has_permission() and self.request.user in task.project.all()



    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.kwargs.get('pk')})


class TaskDelete(PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('webapp:task_list')
    permission_required = 'webapp.task_delete'
    
    def has_permission(self):
        task = self.get_object()
        return super().has_permission() and self.request.user in task.project.all()