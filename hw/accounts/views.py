from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from webapp.models import Project, Task
from webapp.forms import UserUpdate
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
def login_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:task_list')
        context['has_error'] = True
    return render(request, 'login.html', context=context)


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('webapp:task_list')


def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = MyUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('webapp:task_list')
    else:
        form = MyUserCreationForm()
    return render(request, 'user_create.html', context={'form': form})


class UserAdd(PermissionRequiredMixin, UpdateView):
    form_class = UserUpdate
    model = Project
    template_name = 'add_user.html'
    permission_required = 'webapp.user_delete_or_add_perm'

    def has_permission(self):
        return self.request.user.is_superuser or super().has_permission() and self.request.user in self.get_object().user.all()


    def get_success_url(self):
        return reverse('webapp:project_detail', kwargs={'pk': self.kwargs.get('pk')})