from django.shortcuts import render, get_object_or_404
from .models import Category, Project, Post
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import SignUpForm, NewProjectForm, PostForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

class BoardListView(ListView):
    model = Category
    context_object_name = 'boards'
    template_name = 'home.html'

class TopicListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['boards'] = self.boards
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.boards = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        queryset = self.boards.projects.order_by('-date_posted').annotate(replies=Count('posts') - 1)
        return queryset

class PostListView(ListView):
    model = Project
    context_object_name = 'project'
    template_name = 'project_details.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True  

        kwargs['project'] = self.project
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.project = get_object_or_404(Project, category__pk=self.kwargs.get('pk'), pk=self.kwargs.get('project_pk'))
        queryset = self.project.posts.order_by('date_posted')
        return queryset

@login_required
def new_project(request, pk):
    boards = get_object_or_404(Category, pk=pk)

    user = User.objects.first()  # TODO: get the currently logged in user
    
    
    
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
    
        if form.is_valid():
            project = form.save(commit=False)
            project.boards = boards
            project.starter = request.user
            project.save()
            Post.objects.create(
                aims = form.cleaned_data.get('aims'),
                intro = form.cleaned_data.get('intro'),
                proposal = form.cleaned_data.get('proposal'),
                project = project
                
                )
            return redirect('project_details', pk=pk, project_pk=project.pk)  # TODO: redirect to the created topic page
    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {'boards':boards ,'form': form})

def project_details(request, pk, project_pk):
    project = get_object_or_404(Project, category__pk=pk, pk=project_pk)
    project.views += 1
    project.save()
    return render(request, 'project_details.html', {'project': project})

@login_required
def reply_topic(request, pk, project_pk):
    project = get_object_or_404(Project, category__pk=pk, pk=project_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.project = project
            post.user = request.user
            post.save()

            post.date_posted = timezone.now()  # <- here
            post.save()  

            project_url = reverse('project_details', kwargs={'pk': pk, 'project_pk': project_pk})
            project_post_url = '{url}?page={page}#{id}'.format(
                url=project_url,
                id=post.pk,
                page=project.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'project': project, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('aims', 'intro', 'proposal', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('project_details', pk=post.project.boards.pk, project_pk=post.project.pk)