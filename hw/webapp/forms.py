from django import forms
from django.forms import widgets
from webapp.models import Status, Type, Task, Project

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('summary', 'description', 'type_key', 'status_key')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'started_at', 'end_at')


class UserUpdate(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['user',]


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Search')