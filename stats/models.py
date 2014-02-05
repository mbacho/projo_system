from django.db import models

# Create your models here.
class DomainStats(models.Model):
    domain = models.CharField(max_length=100)
    outlinks = models.PositiveIntegerField(default=0)
    richfiles = models.PositiveIntegerField(default=0)
    pages_not_found = models.PositiveIntegerField(default=0)
    page_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return "domain={0},outlinks={1},richfiles={2},pages_not_found={3},page_count={4}".format(
            self.domain, self.outlinks, self.richfiles, self.pages_not_found, self.page_count
        )

    def __str__(self):
        return self.__unicode__()