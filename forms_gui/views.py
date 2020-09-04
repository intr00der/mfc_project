import os

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import FormButton, FormBody, FormField, UsersRequest
from django.views.generic import ListView
from django.core.mail import EmailMessage


class ButtonMixin:
    queryset = FormButton.objects.all()
    template_name = os.path.join('forms_gui', 'buttons.html')
    context_object_name = 'buttons'
    is_start_page = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['button_title'] = ('МНОГОФУНКЦИОНАЛЬНЫЙ ЦЕНТР' if self.is_start_page else
                                   FormButton.objects.get(pk=self.kwargs['id']))
        return context


class HomeView(ButtonMixin, ListView):
    queryset = FormButton.objects.filter(parent__isnull=True)


class ButtonView(ButtonMixin, ListView):
    is_start_page = False

    def get_queryset(self):
        return super().get_queryset().filter(
            parent_id=self.kwargs['id']
        )


class FormBodyView(ListView):
    template_name = os.path.join('forms_gui', 'form_fields.html')
    context_object_name = 'form_fields'
    queryset = FormField.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            form_body__id=self.kwargs['form_id']
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form_body_title'] = FormBody.objects.get(pk=self.kwargs['form_id']).title
        return context

    def post(self, request, *args, **kwargs):
        data = self.prepare_post_data(request.POST)
        form = FormBody.objects.get(pk=self.kwargs['form_id'])
        required_fields = form.form_fields.filter(required=True).values_list('id', flat=True)
        data_keys = set(map(int, {*data.keys()}))
        if data_keys != {*required_fields}:
            return HttpResponseBadRequest('Не меняйте код элемента')
        UsersRequest.objects.create(data=data, form_body_id=kwargs['form_id'])
        mail = 'ya.ne.kuryu@gmail.com'
        subject = 'МФЦ Сервис'
        message = 'Новые данные по заполнению форм: ' + str(data)
        email_from = settings.DEFAULT_EMAIL_FROM
        msg = EmailMessage(subject, message, email_from, [mail])
        msg.send()
        return HttpResponseRedirect(reverse('success'))

    @staticmethod
    def prepare_post_data(data):
        data = dict(data)
        del data['consent']
        del data['approval']
        del data['csrfmiddlewaretoken']
        return {key: value[0] for key, value in data.items()}


def success_page(request):
    return render(request, template_name='forms_gui/success.html')
