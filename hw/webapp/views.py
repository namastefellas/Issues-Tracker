from django.shortcuts import render, redirect, get_object_or_404, reverse
from webapp.models import Task
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView
from django.db.models import Q
from django.utils.http import urlencode


from webapp.forms import TaskForm, SearchForm
from webapp.base_view import CustomFormView



# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'
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


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, id=kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class TaskCreate(CustomFormView):
    template_name = 'task_create.html' 
    form_class = TaskForm
    redirect_url = 'task_list'

    def form_valid(self, form):
        types = form.cleaned_data.pop('type_key')
        task = Task()
        for key, value in form.cleaned_data.items():
            setattr(task, key, value)

        task.save()
        task.type_key.set(types)

        return super().form_valid(form)


class TaskEdit(FormView):
    form_class = TaskForm
    template_name = 'task_edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_object(self):
        task = get_object_or_404(
            Task, id=self.kwargs.get('pk')
            )
        return task

    def form_valid(self, form):
        types = form.cleaned_data.pop('type_key')
        form.save()
        self.task.type_key.set(types)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.kwargs.get('pk')})


class TaskDelete(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        return render(request, 'task_delete.html', {'task': task})
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        task.delete()
        return redirect('task_list')
        


            
