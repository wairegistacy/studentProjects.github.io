from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    name = models.CharField(max_length=30, unique=True)
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
    teacherInChargeEmail = models.CharField(max_length=255, null=True)
    principalName = models.CharField(max_length=255, null=True)
    principalPhone = models.CharField(max_length=255, null=True)
    principalEmail = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete='models.DO_NOTHING', null=True, related_name='categories')
    starter = models.ForeignKey(User, on_delete='models.DO_NOTHING', null=True, related_name='categories')
    last_updated = models.DateTimeField(auto_now_add=True, null=True)

class ProjectInfo(models.Model):
    intro = models.TextField(max_length=4000)
    aims = models.TextField(max_length=4000)
    proposal = models.TextField(max_length=4000)
    project = models.ForeignKey(Project, on_delete='models.DO_NOTHING', related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete='models.DO_NOTHING', related_name='projects')
    updated_by = models.ForeignKey(User, null=True, on_delete='models.DO_NOTHING', related_name='+')
