from django.shortcuts import render
from webapp.models import Task
from django.views.generic import View, TemplateView, RedirectView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    
