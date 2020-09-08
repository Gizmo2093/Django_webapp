from django.shortcuts import render
from .models import Topic
from .forms import TopicForm, EntryForm

from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'blogs/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request,'blogs/topics.html', context)


def topic(request, topic_id):
    #Display one topic and all related entries
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request,'blogs/topic.html', context)

def new_topic(request):
    #Defines a new topic
    if request.method != 'POST':
        #If data was not send - than create empty form 
        form = TopicForm()
    else:
        #if get POST - than processing
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'blogs/new_topic.html', context)


def new_entry(request, topic_id):
    #Added new entry in specific topic
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #If data was not send - than create empty form
        form = EntryForm()
    else:
        #if get POST - than processing
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'blogs/new_entry.html', context)
    
