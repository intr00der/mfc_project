import os
import json

import pdfkit
from random import randint
import datetime

from django.conf import settings
from django.core.files import File
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.contrib.auth.models import User

from .models import FormButton, FormBody, FormField, UsersRequest
from django.views.generic import ListView
from django.core.mail import EmailMessage


# from .utils import render_to_pdf


class ButtonMixin:
    queryset = FormButton.objects.all()
    template_name = os.path.join('forms_gui', 'buttons.html')
    button_title = 'МНОГОФУНКЦИОНАЛЬНЫЙ ЦЕНТР'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['button_title'] = (self.button_title or
                                   FormButton.objects.get(pk=self.kwargs['id']))
        return context

    def get_context_object_name(self, object_list):
        first_object = object_list.first()
        if isinstance(first_object, FormBody):
            return 'form_bodies'
        elif isinstance(first_object, FormButton):
            return 'buttons'
        return None


class HomeView(ButtonMixin, ListView):
    def get_queryset(self):
        form_buttons = self.queryset.filter(parent__isnull=True)
        return form_buttons or FormBody.objects.all()


class ButtonView(ButtonMixin, ListView):
    button_title = None

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

        required_fields = set(map(str, form.form_fields.filter(required=True).values_list('id', flat=True)))
        data_item_list = list(data.items())
        for obj in data_item_list:
            key = obj[0]
            values_list = obj[1]
            model_ref = FormField.objects.get(pk=obj[0])

            if key in required_fields:
                if not values_list:
                    return HttpResponseBadRequest(
                        'Не меняйте код элементов (снятие свойства необходимости заполнения форм)')

            if model_ref.data:
                for value in values_list:
                    if value not in model_ref.data:
                        return HttpResponseBadRequest('Не меняйте код элементов (подмена значения)')
                    value.replace(value, f'{model_ref.title}: {value}')

        users_request = UsersRequest.objects.create(data=json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False),
                                                    form_body_id=kwargs['form_id'])
        template = get_template('forms_gui/invoice.html')
        html = template.render({'data': data})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        options = {
            'encoding': "UTF-8"
        }
        pdf_filename = f'{form.title}_{users_request.number}.pdf'
        msg_output_path = os.path.join(settings.USER_REQUESTS_TEMPORARY_ROOT, pdf_filename)
        pdfkit.from_string(html, msg_output_path, options=options, configuration=config)

        with open(msg_output_path, 'rb') as pdf_file:
            django_file = File(pdf_file)
            users_request.pdf_file.save(pdf_filename, django_file, save=True)

            subject = 'МФЦ Сервис'
            message = 'Новые данные по заполнению форм: '
            admin_email_list = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
            email_from = settings.DEFAULT_EMAIL_FROM

            msg = EmailMessage(subject, message, email_from, admin_email_list)
            msg.attach_file(msg_output_path)
            msg.send()
        return HttpResponseRedirect(reverse('success'))

    @staticmethod
    def prepare_post_data(data):
        data = dict(data)
        del data['consent']
        del data['approval']
        del data['csrfmiddlewaretoken']
        return {key: value for key, value in data.items()}


def success_page(request):
    return render(request, template_name='forms_gui/success.html')
