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
        #context['form_body_title'] = FormBody.objects.get(pk=self.kwargs['form_id']).title
        return context

    @staticmethod
    def validate_form_data(form_data, form_body):
        error_msg = None
        dom_changed_msg = 'Не меняйте код элемента'
        field_options = {str(field.id): field.options for field in form_body.form_fields.all()}

        required_field_ids = set(map(str, form_body.form_fields.filter(required=True).values_list('id', flat=True)))

        is_valid = True
        # Валидация
        for field_id, field_values in form_data.items():
            if field_id in required_field_ids:
                if not field_values:
                    is_valid = False
                    error_msg = dom_changed_msg
                    break

            if field_options[field_id]:
                for value in field_values:
                    if value not in field_options[field_id]:
                        is_valid = False
                        error_msg = dom_changed_msg
                        break
                if not is_valid:
                    break
        return is_valid, error_msg

    def post(self, request, *args, **kwargs):
        form_data = self.prepare_form_data(request.POST)
        form_body = FormBody.objects.get(pk=self.kwargs['form_id'])

        is_valid, error_msg = self.validate_form_data(form_data, form_body)
        if not is_valid:
            return HttpResponseBadRequest(error_msg)

        users_request = UsersRequest.objects.create(data=json.dumps(form_data, sort_keys=True, indent=2, ensure_ascii=False),
                                                    form_body_id=kwargs['form_id'])
        template = get_template('forms_gui/invoice.html')
        html = template.render({'data': form_data, 'body': str(form_body)})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        options = {
            'encoding': "UTF-8"
        }
        pdf_filename = f'{form_body.title}_{users_request.number}.pdf'
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
    def prepare_form_data(data):
        data = dict(data)
        del data['consent']
        del data['approval']
        del data['csrfmiddlewaretoken']
        return data


def success_page(request):
    return render(request, template_name='forms_gui/success.html')
