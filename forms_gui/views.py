from django.shortcuts import render
from .models import FormBody, FormField, FormButton
from django.views.generic import CreateView, ListView, View


class HomeView(ListView):

    def get_queryset(self):
        queryset = {
            FormButton.objects.all()
        }
        return render('form_fields.html', {'queryset': queryset})
