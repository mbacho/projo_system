from django.db import models

# Create your models here.


class AcademicDomain(models.Model):
    """Valid domain for academic institutions"""
    name = models.CharField(max_length=150)
    domain = models.CharField(max_length=255)
    link = models.URLField()

    def __unicode__(self):
        return u'{0} ({1} | {2})'.format(self.name, self.domain, self.link)


class AvoidUrl(models.Model):
    domain = models.ForeignKey(AcademicDomain, related_name='avoidurl_domain')
    url_pattern = models.CharField(unique=True, null=False, blank=False, max_length=100)

    def __unicode__(self):
        return u'{0} "{1}"'.format(self.domain.domain, self.url_pattern)


class RichFile(models.Model):
    name = models.CharField(max_length=255)
    ext = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=255)
