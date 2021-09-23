import logging

import requests
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_fsm import can_proceed

from service_catalog.forms import MessageOnRequestForm, AcceptRequestForm
from service_catalog.mail_utils import send_mail_request_update
from service_catalog.models import Request, RequestState

logger = logging.getLogger(__name__)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_need_info(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    parameters = {
        'request_id': target_request.id,
        'message_required': True
    }
    if request.method == "POST":
        form = MessageOnRequestForm(request.user, request.POST, **parameters)
        if form.is_valid():
            # check that we can ask for info the request
            if not can_proceed(target_request.need_info):
                raise PermissionDenied
            form.save()
            target_request.need_info()
            target_request.save()
            message = form.cleaned_data['message']
            send_mail_request_update(target_request, user_applied_state=request.user, message=message)
            return redirect('service_catalog:request_list')
    else:
        form = MessageOnRequestForm(request.user, **parameters)
    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
    ]
    context = {
        'form': form,
        'target_request': target_request,
        'breadcrumbs': breadcrumbs
    }
    return render(request, "service_catalog/admin/request/request-need-info.html", context)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_re_submit(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    parameters = {
        'request_id': target_request.id,
        'message_required': False
    }
    if request.method == "POST":
        form = MessageOnRequestForm(request.user, request.POST, **parameters)
        if form.is_valid():
            if not can_proceed(target_request.re_submit):
                raise PermissionDenied
            form.save()
            target_request.re_submit()
            target_request.save()
            send_mail_request_update(target_request, user_applied_state=request.user)
            return redirect('service_catalog:request_list')
    else:
        form = MessageOnRequestForm(request.user, **parameters)
    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
    ]
    context = {
        'form': form,
        'target_request': target_request,
        'breadcrumbs': breadcrumbs
    }
    return render(request, "service_catalog/admin/request/request-re-submit.html", context)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_reject(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    parameters = {
        'request_id': target_request.id,
        'message_required': True
    }
    if request.method == "POST":
        form = MessageOnRequestForm(request.user, request.POST, **parameters)
        if form.is_valid():
            if not can_proceed(target_request.reject):
                raise PermissionDenied
            form.save()
            target_request.reject()
            target_request.save()
            message = form.cleaned_data['message']
            send_mail_request_update(target_request, user_applied_state=request.user, message=message)
            return redirect('service_catalog:request_list')
    else:
        form = MessageOnRequestForm(request.user, **parameters)
    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
    ]
    context = {
        'form': form,
        'target_request': target_request,
        'breadcrumbs': breadcrumbs
    }
    return render(request, "service_catalog/admin/request/request-reject.html", context)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_accept(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    parameters = {
        'request_id': request_id
    }
    if request.method == 'POST':
        form = AcceptRequestForm(request.user, request.POST, **parameters)
        if form.is_valid():
            form.save()
            target_request.refresh_from_db()
            send_mail_request_update(target_request, user_applied_state=request.user)
            return redirect('service_catalog:request_list')
    else:
        form = AcceptRequestForm(request.user, initial=target_request.fill_in_survey, **parameters)
    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
    ]
    context = {
        'form': form,
        'target_request': target_request,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'service_catalog/admin/request/request-accept.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_process(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    error = False
    error_message = ""
    if request.method == "POST":
        if not can_proceed(target_request.process):
            raise PermissionDenied
        import towerlib
        try:
            # switch the state to processing before trying to execute the process
            target_request.process()
            target_request.save()
            target_request.perform_processing()
            target_request.save()
        except towerlib.towerlibexceptions.AuthFailed:
            error = True
            logger.error(
                f"[admin_request_process] Fail to authenticate with provided token when trying to process request "
                f"id '{target_request.id}'")
            error_message = "Fail to authenticate with provided token"
        except requests.exceptions.SSLError:
            error = True
            error_message = "Certificate verify failed"
            logger.error(
                f"[admin_request_process] Certificate verify failed when trying to process request "
                f"id '{target_request.id}'")
        except requests.exceptions.ConnectionError:
            error = True
            error_message = "Unable to connect to remote server"
            logger.error(
                f"[admin_request_process] Unable to connect to remote server when trying to process request "
                f"id '{target_request.id}'")
        if not error:
            target_request.save()
            send_mail_request_update(target_request, user_applied_state=request.user)
            return redirect('service_catalog:request_list')
    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
    ]
    context = {
        'target_request': target_request,
        'error_message': error_message,
        'breadcrumbs': breadcrumbs
    }
    return render(request, "service_catalog/admin/request/request-process.html", context)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_details(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)

    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
    ]
    context = {'target_request': target_request,
               'breadcrumbs': breadcrumbs,
               }
    return render(request, 'service_catalog/admin/request/request-details.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def admin_request_archive_toggle(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    if target_request.state == RequestState.COMPLETE:
        target_request.archive()
    elif target_request.state == RequestState.ARCHIVED:
        target_request.unarchive()
    target_request.save()
    return redirect('service_catalog:request_list')


@user_passes_test(lambda u: u.is_superuser)
def request_delete(request, request_id):
    target_request = get_object_or_404(Request, id=request_id)
    parameters = {
        'request_id': request_id
    }
    if request.method == 'POST':
        target_request.delete()
        return redirect("service_catalog:request_list")
    breadcrumbs = [
        {'text': 'Requests', 'url': reverse('service_catalog:request_list')},
        {'text': request_id, 'url': ""},
        {'text': "Delete", 'url': ""},
    ]
    context = {
        'breadcrumbs': breadcrumbs,
        'confirm_text': mark_safe(f"Confirm deletion of request <strong>{target_request.id}</strong>?"),
        'action_url': reverse('service_catalog:request_delete', kwargs=parameters),
        'button_text': 'Delete'
    }
    return render(request, 'generics/confirm-delete-template.html', context=context)
