
from django.db import models
from webui.models import ProjectDomain


class DomainStats(models.Model):
    projectdomain = models.ForeignKey(ProjectDomain)

    outlinks = models.PositiveIntegerField(default=0)
    richfiles = models.PositiveIntegerField(default=0)
    pages_not_found = models.PositiveIntegerField(default=0)
    page_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "domain={0},outlinks={1},richfiles={2},pages_not_found={3},page_count={4}".format(
            self.projectdomain, self.outlinks, self.richfiles, self.pages_not_found, self.page_count
        )
