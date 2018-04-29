from django.shortcuts import render, redirect
from django.core.exceptions import *
from django.contrib import *
from django.urls import reverse
from django.http import *
from tasks.models import *
from tasks.forms import *

context = {}


def get_task_list(request):
    context['page_title'] = 'Task List'
    context['task_list'] = Task.objects.all()
    context['form'] = TaskForm(instance=Task())

    handle_request(request)

    return render(request, 'task_list.html', context)


def handle_request(request):
    if request.method == 'GET':
        request_to_lowercase = {k.lower(): v.lower() for k, v in request.GET.items()}
        try:
            action = request_to_lowercase['action']
        except Exception:
            return

        if (action == 'delete'):
            delete_task(request_to_lowercase, request)
        elif (action == 'done'):
            task_done(request_to_lowercase, request)

    elif request.method == 'POST':
        create_task(request)


def delete_task(request_dict, request):
    try:
        request_get_id = int(request_dict['id'])
        instance = Task.objects.get(pk=request_get_id)
    except ObjectDoesNotExist:
        messages.error(request, u'Task does not exist.')
        return
    except KeyError:
        messages.error(request, u'Data incorrect.')
        return

    instance.delete()


def task_done(request_dict, request):
    try:
        request_get_id = int(request_dict['id'])
        request_get_value = request_dict['value']
        task_to_update = Task.objects.get(pk=request_get_id)
    except ObjectDoesNotExist:
        messages.error(request, u'Task does not exist.')
        return
    except KeyError:
        messages.error(request, u'Data incorrect.')
        return

    task_done_value = task_to_update.done

    if (request_get_value == 'true'):
        task_done_value = True
    elif (request_get_value == 'false'):
        task_done_value = False

    task_to_update.done = task_done_value

    task_to_update.save()


def create_task(request):
    form = TaskForm(request.POST, instance=Task())
    form_valid_handler(request, form)
    context['form'] = form


def form_valid_handler(request, form):
    if form.is_valid():
        form.save()
        messages.success(request, u'Task successfully saved')
    else:
        messages.error(request, u'Data incorrect')
        pass
