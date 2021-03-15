from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Task
from django.views.generic import View, TemplateView, RedirectView
from webapp.forms import TaskForm

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        kwargs['tasks'] = Task.objects.all()
        return super().get_context_data(**kwargs)


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, id=kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class TaskCreate(View):

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'task_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task=Task.objects.create(
                summary=form.cleaned_data.get("summary"),
                description=form.cleaned_data.get("description"),
                status_key=form.cleaned_data.get("status_key")
            )
            task.type_key.set(form.cleaned_data.get('type_key'))
            return redirect('task_view', pk=task.pk)
        else:
            return redirect('task_create.html', context={'form': form})


class TaskEdit(View):

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        form = TaskForm(initial={
            'summary': task.summary,
            'description': task.description,
            'status_key': task.status_key,
            'type_key': task.type_key.all()
        })
        return render(request, 'task_edit.html', {'form': form, 'task': task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.summary = form.cleaned_data['summary']
            task.description = form.cleaned_data['description']
            task.status_key = form.cleaned_data['status_key']
            task.type_key.set(form.cleaned_data.get('type_key'))
            task.save()

            return redirect('task_view', pk=kwargs.get('pk'))
        else:
            return redirect(request, 'task_edit.html', context={'form': form})


class TaskDelete(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        return render(request, 'task_delete.html', {'task': task})
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        task.delete()
        return redirect('task_list')
        


            
