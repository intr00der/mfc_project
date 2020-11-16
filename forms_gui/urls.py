from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from conf.decorators import for_staff_only
from .views import HomeView, ButtonView, FormBodyView, success_page


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('button/<int:id>', ButtonView.as_view(), name='form-button'),
    path('form/<int:form_id>', FormBodyView.as_view(), name='form-body'),
    path('success', success_page, name='success'),
] + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    ) + \
    static(
        settings.USER_REQUESTS_URL,
        for_staff_only(serve),
        document_root=settings.USER_REQUESTS_ROOT
    )
