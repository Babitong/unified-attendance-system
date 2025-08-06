from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import Http404

from .models import Question, Choice

# get questions and display those questions


def index(request):
    return render(request, 'index.html')

# Create your views here.
