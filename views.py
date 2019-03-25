from django.shortcuts import render, get_object_or_404
from .models import Project, Participant, School, Project_Information, Project_Proposals
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .forms import Meta

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
    boards = Project.objects.all()
    return render(request, 'home.html', {'boards': boards})

def project_participants(request, pk):
    boards = Project.objects.get(pk=pk)
    return render(request, 'topics.html', {'boards': boards})

def new_project(request, pk):
    boards = get_object_or_404(Project, pk=pk)
    return render(request, 'new_project.html', {'boards': boards})
