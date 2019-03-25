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

class Project(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Participant(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete='models.DO_NOTHING', related_name='participant')
    starter = models.ForeignKey(User, on_delete='models.DO_NOTHING',related_name='participant')
   
class School(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    participant = models.ForeignKey(Participant, on_delete='models.DO_NOTHING', related_name='school')
    starter = models.ForeignKey(User, on_delete='models.DO_NOTHING',related_name='school')
   
class Project_Information(models.Model):
    message = models.TextField(max_length=4000)
    school = models.ForeignKey(School, on_delete='models.DO_NOTHING', related_name='project_information')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete='models.DO_NOTHING', related_name='project_information')
    updated_by = models.ForeignKey(User, on_delete='models.DO_NOTHING', null=True, related_name='+')
    
class Project_Proposals(models.Model):
    message = models.TextField(max_length=4000)
    project_information = models.ForeignKey(Project_Information, on_delete='models.DO_NOTHING', related_name='project_proposals'),
    created_at = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(null=True),
    created_by = models.ForeignKey(User, on_delete='models.DO_NOTHING', related_name='project_proposals'),
    updated_by = models.ForeignKey(User, on_delete='models.DO_NOTHING', null=True, related_name='+'),
    