from django.conf.urls import url, include
from . import views

urlpatterns = [
            url(r'^$', views.index, name="index"),
            url(r'^index$', views.index, name="index_2"),
            url(r'^batches/$', views.batches, name="view_batch"),
            url(r'^module/(?P<pk>[0-9]+)/(?P<start>[0-9]+)/(?P<delta>[0-2]+)/$', views.view_module, name="view_module"),
            url(r'^module/new/$', views.new_module, name='new_module')
]
