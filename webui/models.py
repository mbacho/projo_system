from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now

from johnnywalker.models import AcademicDomain


class Project(models.Model):
    """Project details"""
    RUN_FREQ = (
        ('none', 'none'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
    )

    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='projects')
    desc = models.TextField(blank=True, null=True)
    freq = models.CharField(max_length=10, choices=RUN_FREQ, default='none')

    class Meta:
        unique_together = ('name', 'owner')
        ordering = ['-created']

    def __unicode__(self):
        return unicode(self.name)


class ProjectDomain(models.Model):
    JOB_STATUS = (
        ('running', 'running'),
        ('finished', 'finished'),
        ('cancelled', 'cancelled'),
        ('shutdown', 'shutdown'),
        ('unknown', 'unknown'),
        ('error', 'error'),
        ('paused', 'paused'),
    )
    project = models.ForeignKey(Project, related_name='projectdomain_project')
    domain = models.ForeignKey(AcademicDomain, related_name='projectdomain_domain')

    subdomain = models.CharField(default='', null=True, blank=True, max_length=50)
    starturl = models.URLField(null=True, blank=True)
    jobid = models.CharField(max_length=100, default='', blank=True, unique=True)
    starttime = models.DateTimeField(auto_now_add=True, default=now())
    stoptime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='unknown', blank=True, choices=JOB_STATUS)

    @property
    def get_crawl_domain(self):
        return self.domain.domain if self.subdomain == '' else self.subdomain + "." + self.domain.domain

    @property
    def get_collection_name(self):
        return self.jobid or self.domain

    @property
    def get_runtime(self):
        if self.stoptime:
            return self.stoptime - self.starttime
        return now() - self.starttime

    def __unicode__(self):
        return u"{0} {1}.{2} {3}".format(self.project, self.subdomain, self.domain, self.jobid)
