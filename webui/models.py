from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone
from johnnywalker.models import AcademicDomain


class Project(models.Model):
    """Project details"""
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.name)


class UserDets(models.Model):
    """Stores user details"""
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.user.get_username())


class ProjectDomains(models.Model):
    project = models.ForeignKey(Project)
    domain = models.ForeignKey(AcademicDomain)
    jobid = models.CharField(max_length=100, default='')
    start = models.DateTimeField(auto_now_add=True, default=timezone.now())
    stop = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=20, default='')

    def __unicode__(self):
        return u"{0}".format(self.project, self.domain, self.jobid)