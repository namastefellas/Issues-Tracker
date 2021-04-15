from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from webapp.models import Project
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User



from webapp.forms import ProjectForm, SearchForm
from webapp.base_view import CustomFormView


class ProjectView(ListView):
    template_name = 'project/project.html'
    model = Project
    context_object_name = 'projects'
    ordering = ('name', '-started_at')

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(ProjectView, self).get(request, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data) |
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



class ProjectDetail(DetailView):
    model = Project
    template_name = 'project/project_view.html'


class ProjectCreate(PermissionRequiredMixin, CreateView):
    template_name = 'project/project_create.html' 
    model = Project
    form_class = ProjectForm
    permission_required = 'webapp.project_create'

    def form_valid(self, form):
        user = self.request.user
        project = form.save()
        project.user.add(user)
        return redirect('webapp:project_detail', pk=project.pk)




    # def get_success_url(self):
    #     return reverse('webapp:project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'project/project_edit.html'
    context_object_name = 'project'
    permission_required = 'webapp:project_edit'

    def get_success_url(self):
        return reverse('webapp:project_detail', kwargs={'pk': self.kwargs.get('pk')})


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('webapp:project_view')
    permission_required = 'webapp:project_delete'