from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from accounts.models import Profile
from accounts.forms import UserUpdateFrom, ProfileUpdateForm, UserChangePasswordForm

class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user_profile.html'
    context_object_name = 'user'
    paginate_related_by = 3
    paginate_related_orphans = 1

    def get_context_data(self, **kwargs):
        projects = self.object.projects.all().order_by('-started_at')
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
  
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        kwargs['profile'] = get_object_or_404(Profile, user__pk=self.kwargs.get('pk'))
        print(kwargs['profile'])
        return super().get_context_data(**kwargs)


class UserList(PermissionRequiredMixin, ListView):
    template_name = 'user_list.html'
    model = get_user_model()
    context_object_name = 'users'
    ordering = ('username',)
    permission_required = 'accounts.user_view'

    def has_permission(self):
        return super().has_permission()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_update.html'
    context_object_name = 'user_obj'
    form_class = UserUpdateFrom

    profile_form_class = ProfileUpdateForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        user_form = self.get_form()
        profile_form = self.get_profile_form()

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        return self.form_invalid(user_form, profile_form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['profile_form'] = kwargs.get('profile_form')
        if context['profile_form'] is None:
            context['profile_form'] = self.get_profile_form()
        return context

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(
            form=user_form,
            profile_form=profile_form
        )

        return self.render_to_response(context)

    def form_valid(self, user_form, profile_form):
        response = super(UserUpdateView, self).form_valid(user_form)

        profile_form.save()
        return response

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}

        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return self.profile_form_class(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={'pk': self.object.pk})


class UserChangePasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'user_change_password.html'
    model = get_user_model()
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super(UserChangePasswordView, self).form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        return response

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={'pk': self.object.pk})