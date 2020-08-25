import os

from .models import FormButton, FormBody, FormField
from django.views.generic import ListView


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
    context_object_name = 'form_bodies'
    queryset = FormBody.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            id=self.kwargs['form_id']
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
        context['form_body_title'] = FormBody.objects.get(pk=self.kwargs['form_id'])
        return context
