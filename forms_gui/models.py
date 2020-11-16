import os

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage
from django.db import models, transaction
from django.db.models import JSONField
from mptt.models import MPTTModel, TreeForeignKey

from conf.settings import USER_REQUESTS_ROOT, USER_REQUESTS_URL


class FormField(models.Model):
    FORM_TYPE_CHOICES = [('text', 'Текст'),
                         ('radio', 'Радио кнопки'),
                         ('dropdown', 'Выпадающий список'),
                         ('date', 'Поле даты'),
                         ('checkbox', 'Чекбокс')]

    title = models.CharField('Название поля', max_length=255)
    type = models.CharField('Тип поля', max_length=31, choices=FORM_TYPE_CHOICES)
    data = ArrayField(models.CharField(max_length=31), blank=True, null=True)
    details = models.CharField('Поясняющий текст', max_length=255, blank=True, null=True)
    required = models.BooleanField('Обязательное ли поле', default=False)

    class Meta:
        verbose_name = 'Поле справки'
        verbose_name_plural = 'Поля справок'

    def __str__(self):
        return self.title


class FormBody(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    details = models.CharField('Поясняющий текст для справки',
                               max_length=255, blank=True, null=True)
    form_fields = models.ManyToManyField(FormField, verbose_name='Поля справки',
                                         related_name='form_body')

    class Meta:
        default_related_name = 'form_bodies'
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    def __str__(self):
        return self.title


class FormButton(MPTTModel):
    title = models.CharField('Заголовок группы', max_length=255, blank=True, null=True)
    parent = TreeForeignKey('self',
                            verbose_name='К какой группе относится',
                            null=True,
                            blank=True,
                            related_name='children',
                            on_delete=models.CASCADE,
                            )
    form_body = models.OneToOneField(FormBody,
                                     null=True,
                                     blank=True,
                                     verbose_name='К какой справке ведет',
                                     on_delete=models.CASCADE,
                                     related_name='form_button',
                                     )

    class Meta:
        verbose_name = 'Группа справки'
        verbose_name_plural = 'Группы справок'

    def __str__(self):
        return self.title or ''


user_requests_storage = FileSystemStorage(location=USER_REQUESTS_ROOT, base_url=USER_REQUESTS_URL)


class UsersRequest(models.Model):
    data = JSONField('Данные пользователя')
    form_body = models.ForeignKey(FormBody, on_delete=models.SET_NULL, related_name='users_request', null=True)
    pdf_file = models.FileField("Файл пользовательского запроса", blank=True, null=True, storage=user_requests_storage)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, blank=False)
    number = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователя'

    def identify_request_number(self):
        with transaction.atomic():
            user_requests = UsersRequest.objects.select_for_update().filter(form_body_id=self.form_body_id)
            try:
                latest_user_request = user_requests.latest('created_at')
            except self.DoesNotExist:
                number = 1
            else:
                number = latest_user_request.number + 1
        return number

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.number = self.identify_request_number()
        super().save(*args, **kwargs)
