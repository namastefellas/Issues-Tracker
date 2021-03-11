from django import forms
from django.forms import widgets

class TaskForm(forms.Form):
    summary = forms.CharField(max_length=100, required=True, label='Summary')
    description = forms.CharField(max_length=400, required=False, label='Description', widget=widgets.Textarea)
    type_choice = forms.ModelChoiceField(queryset=Type.objects.all())
    status_choice = forms.ModelChoiceField(queryset=Status.objects.all())