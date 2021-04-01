from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Task, Project
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.utils.http import urlencode


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


class TaskCreate(CreateView):
    template_name = 'task/task_create.html' 
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('project_detail', pk=self.kwargs.get('pk'))
    

class TaskEdit(UpdateView):
    form_class = TaskForm
    model = Task
    template_name = 'task/task_edit.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.kwargs.get('pk')})


class TaskDelete(DeleteView):
    model = Task
    template_name = 'task/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')


    # def get(self, request, *args, **kwargs):
    #     task = get_object_or_404(Task, id=kwargs.get('pk'))
    #     return render(request, 'task/task_delete.html', {'task': task})
    # def post(self, request, *args, **kwargs):
    #     task = get_object_or_404(Task, id=kwargs.get('pk'))
    #     task.delete()
    #     return redirect('task_list')