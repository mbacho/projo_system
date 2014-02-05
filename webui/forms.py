

from django.forms import ModelForm
from .models import Project


class ProjectEdit(ModelForm):
    class Meta:
        model = Project
