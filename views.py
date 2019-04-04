from django.shortcuts import render, get_object_or_404
from .models import Category, Project, ProjectInfo
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import SignUpForm
from .forms import NewProjectForm
from django.contrib.auth.models import User
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    boards = Category.objects.all()
    return render(request, 'home.html', {'boards': boards})

def category_project(request, pk):
    boards = Category.objects.get(pk=pk)
    return render(request, 'topics.html', {'boards': boards})

def new_project(request, pk):
    boards = get_object_or_404(Category, pk=pk)
   
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('category_project', pk=boards.pk)  # TODO: redirect to the created topic page
    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {'boards': boards, 'form': form})

def project_details(request):
    boards = Project.objects.all()
    return render(request, 'project_details.html', {'boards': boards})
