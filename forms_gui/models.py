from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class FormField(models.Model):
    FORM_TYPE_CHOICES = [('text', 'Текст'),
                         ('radio', 'Радио кнопки'),
                         ('dropdown', 'Выпадающий список'),
                         ('date', 'Поле даты'),
                         ('checkbox', 'Чекбокс')]

    title = models.CharField('Название поля', max_length=255)
    type = models.CharField('Тип поля', max_length=31, choices=FORM_TYPE_CHOICES)
    data = models.TextField('Тело формы', blank=True, null=True)  # Для radio, dropdown
    details = models.CharField('Поясняющий текст', max_length=255, blank=True, null=True)
    required = models.BooleanField('Обязательное ли поле', default=False)

    class Meta:
        verbose_name = 'Поле справки'
        verbose_name_plural = 'Поля справок'

    def data_as_list(self):
        return str(self.data).split('\n')

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
