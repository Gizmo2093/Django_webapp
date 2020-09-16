from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'blogs/index.html')


@login_required
def topics(request):
    #Display list topics
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request,'blogs/topics.html', context)


@login_required
def topic(request, topic_id):
    #Display one topic and all related entries
    topic = Topic.objects.get(id=topic_id)
    #Check owner topic
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request,'blogs/topic.html', context)


@login_required
def new_topic(request):
    #Defines a new topic
    if request.method != 'POST':
        #If data was not send - than create empty form 
        form = TopicForm()
    else:
        #if get POST - than processing
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'blogs/new_topic.html', context)


@login_required
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
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'blogs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    #Editing existing entry
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    #Check owner for edit entry
    if topic.owner != request.user:
        raise Http404
    #Check data, form full in origin data
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        #send data POST, processing
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'blogs/edit_entry.html', context)
