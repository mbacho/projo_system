from django.conf.urls import (patterns, url)
from .views import results

urlpatterns = patterns('',
                       url(r'^results/', results, name='results'),
                       url(r'^stats/([0-9]+)/', results, name='results_det'),
)
