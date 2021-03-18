from django import forms
from django.forms import widgets
from webapp.models import Status, Type, Task

class TaskForm(forms.ModelForm):
    summary = forms.CharField(max_length=100, required=True, label='Summary')
    description = forms.CharField(max_length=400, required=False, label='Description', widget=widgets.Textarea)
    type_key = forms.ModelMultipleChoiceField(queryset=Type.objects.all())
    status_key = forms.ModelChoiceField(queryset=Status.objects.all())

    class Meta:
        model = Task
        fields = ('summary', 'description', 'type_key', 'status_key')