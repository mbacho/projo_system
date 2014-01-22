from django.db import models

# Create your models here.


class AcademicDomain(models.Model):
    """Valid domain for academic institutions"""
    name = models.CharField(max_length=150)
    # abbr = models.CharField(max_length=50)
    domain = models.URLField()
    link = models.URLField()


class DomainAvoidUrl(models.Model):
    domain = models.ForeignKey(AcademicDomain)
    url_pattern = models.CharField(unique=True, null=False, blank=False,max_length=100)
