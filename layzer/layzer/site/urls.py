"Layzer urls"

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url('^$', views.home, name='home'),
    url('^login/$', views.login, name='login'),
    url('^logout/$', views.logout, name='logout'),
)
