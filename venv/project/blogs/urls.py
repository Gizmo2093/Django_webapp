from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    
    #Home page
    path("", views.index, name='index'),

    #Page for display all topics
    path("topics/", views.topics, name='topics'),

    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    #Page for create new topic
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    #Page for create new entry
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
]
