import math
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name

class Project(models.Model):
    topic = models.CharField(max_length=255, null=True)
    firstParticipant = models.CharField(max_length=255, null=True)
    secondParticipant = models.CharField(max_length=255, null=True)
    schoolName = models.CharField(max_length=255, null=True)
    level = models.CharField(max_length=255, null=True)
    teacherInChargeName = models.CharField(max_length=255, null=True)
    teacherInChargePhone = models.CharField(max_length=255, null=True)
    teacherInChargeEmail = models.EmailField(max_length=255, null=True)
    principalName = models.CharField(max_length=255, null=True)
    principalPhone = models.CharField(max_length=255, null=True)
    principalEmail = models.EmailField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete='models.CASCADE', null=True, related_name='projects' )
    user = models.ForeignKey(User, on_delete='models.CASCADE', null=True, related_name='projects')
    date_posted = models.DateTimeField(default=timezone.now, null=True)
    
    def __str__(self):
        return self.topic

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-date_posted')[:10]
    
    def get_absolute_url(self):
        return reverse(
            "topic:detail",
            kwargs={
                "slug": self.slug,
                "pk": self.pk
            }
        )

class Post(models.Model):
    intro = models.TextField()
    aims = models.TextField()
    proposal = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now, null=True)
    category = models.ForeignKey(Category, on_delete='models.CASCADE', null=True)
    project = models.ForeignKey(Project, on_delete='models.CASCADE', null=True, related_name='posts')
    user = models.ForeignKey(User, on_delete='models.CASCADE', null=True)

    def __str__(self):
        truncated_intro = Truncator(self.intro)
        return truncated_intro.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.aims, safe_mode='escape'))
        return mark_safe(markdown(self.intro, safe_mode='escape'))
        return mark_safe(markdown(self.proposal, safe_mode='escape'))
        return mark_safe(markdown(self.intro, safe_mode='escape'))
        