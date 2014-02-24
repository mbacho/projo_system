from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone
from johnnywalker.models import AcademicDomain


class Project(models.Model):
    """Project details"""
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='projects')

    def __unicode__(self):
        return unicode(self.name)


class ProjectDomain(models.Model):
    project = models.ForeignKey(Project, related_name='projectdomain_project')
    domain = models.ForeignKey(AcademicDomain, related_name='projectdomain_domain')

    subdomain = models.CharField(default='', null=True, blank=True, max_length=50)
    starturl = models.URLField(null=True, blank=True)
    jobid = models.CharField(max_length=100, default='')
    starttime = models.DateTimeField(auto_now_add=True, default=timezone.now())
    stoptime = models.DateTimeField(null=True, blank=True)
    stopreason = models.CharField(max_length=20, default='')

    def __unicode__(self):
        return u"{0} {1}.{2} {3}".format(self.project, self.subdomain, self.domain, self.jobid)