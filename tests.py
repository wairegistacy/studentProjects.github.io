from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home, category_project
from .models import Category, Project, Post

#create your tests here

class HomeTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve ('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        project_participants_url = reverse('project_participants', kwargs={'pk': self.project.pk})
        self.assertContains(self.response, 'href="{0}"'.format(b_url))
       
class CategoryProjectTests(TestCase):
    def setUp(self):
        Category.objects.create(name='Chemical, physical and mathematical sciences',description='These projects deal with the chemical, physical and behavioural fields')

    def test_category_project_view_success_status_code(self):
        url = reverse('category_project', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category_project_view_not_found_status_code(self):
        url = reverse('category_project', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_category_project_url_resolves_project_participants_view(self):
        view = resolve('/project/1/')
        self.assertEquals(view.func, 'category_project')

    def test_project_participants_view_contains_link_back_to_homepage(self):
        project_participants_url = reverse('project_participants', kwargs={'pk': 1})
        response = self.client.get(project_participants_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

class NewTopicTests(TestCase):
    def setUp(self):
        Category.objects.create(name='Chemical, physical and mathematical sciences', description='These projects are for chemistry, physical and mathematical fields')

    def test_new_project_view_success_status_code(self):
        url = reverse('new_project', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_project_view_not_found_status_code(self):
        url = reverse('new_project', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_project_url_resolves_new_project_view(self):
        view = resolve('/project/1/new/')
        self.assertEquals(view.func, new_project)

    def test_new_project_view_contains_link_back_to_project_participants_view(self):
        new_project_url = reverse('new_project', kwargs={'pk': 1})
        project_participants_url = reverse('project_participants', kwargs={'pk': 1})
        response = self.client.get(new_project_url)
        self.assertContains(response, 'href="{0}"'.format(project_participants_url))