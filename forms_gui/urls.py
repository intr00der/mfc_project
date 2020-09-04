from django.urls import path
from .views import HomeView, ButtonView, FormBodyView, success_page

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('button/<int:id>', ButtonView.as_view(), name='form-button'),
    path('button/<int:button_id>/form/<int:form_id>',
         FormBodyView.as_view(),
         name='form-body'),
    path('success', success_page, name='success'),
]
