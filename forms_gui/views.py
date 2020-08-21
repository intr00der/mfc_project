import os

from .models import FormButton
from django.views.generic import ListView


class HomeView(ListView):
    queryset = FormButton.objects.filter(parent__isnull=True)
    template_name = os.path.join('forms_gui', 'home.html')
    context_object_name = 'buttons'


class ButtonView(ListView):
    queryset = FormButton.objects.all()
    template_name = os.path.join('forms_gui', 'buttons.html')
    context_object_name = 'buttons'

    def get_queryset(self):
        return super().get_queryset().filter(
            parent_id=self.kwargs['id']
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['button_title'] = FormButton.objects.get(pk=self.kwargs['id'])
        return context


class FormBodyView(ListView):
    pass
