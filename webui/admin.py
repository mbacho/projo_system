from django.contrib import admin
from .models import (Project,ProjectDomains,UserDets)

admin.site.register(Project)
admin.site.register(ProjectDomains)
admin.site.register(UserDets)

