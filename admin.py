from django.contrib import admin
from .models import Category, Project, Post

# Register your models here.
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Post)
