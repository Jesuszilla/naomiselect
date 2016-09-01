from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getROMList$', views.getROMList, name='getROMList'),
    url(r'^selectROM$', views.selectROM, name='selectROM'),
]
