from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Image, Task, EventLog
from django.forms.models import inlineformset_factory, modelformset_factory
from .decorators import timeout_logging
from forms import MenuItemForm
from django.db import models
from django import forms
from django.conf import settings
import user_patch

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    return HttpResponseRedirect(reverse('data:menus'))


@login_required(login_url="/login/")
def list_images(request):
    images = request.user.get_tasks()
    context = {
        'images': images,
    }
    return render(request, "data/menus.html", context)


def field_widget_callback(field):
    return forms.TextInput(attrs={'placeholder': field.name})

@timeout_logging
def task_entry(request, task_id):
    inactive = 0
    task = Task.objects.get(id=task_id, user_id=request.user.id)
    TaskFormset = modelformset_factory(Task, max_num=1)
    # Evaluate which form the post came from.  If from timer, then repopulate with request.DATA
    # else save it per usual
    if request.method == "POST":
        print "GUID: {}".format(request.POST['seconds'])
        taskformset = TaskFormset(request.POST, request.FILES)
        if request.POST['action'] == "+" or request.POST['action'] == "submit":
            if taskformset.is_valid():
                entryformset.save()
                if request.POST['action'] == "submit":
                    return HttpResponseRedirect(reverse('data:images'))

        if request.POST['action'] == "log":
            inactive = 1

    else:
        taskformset = TaskFormset()


    context = {
        'inactive': inactive,
        'task': task,
        'taskformset': taskformset,
        'DEBUG': settings.DEBUG,
    }
    return render(request, "data/menu_entry.html", context)

@login_required(login_url="/login/")
def log_event(request, task_id):
    task = Task.objects.get(id=task_id, user_id=request.user.id)
    url = "/menuentry/{}".format(menu_id)
    event = EventLog(task_id=task.id, name="timeout")
    event.save()
    return redirect(url)
