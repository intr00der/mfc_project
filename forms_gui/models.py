from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class FormField(models.Model):
    FORM_TYPE_CHOICES = [('text', 'Текст'),
                         ('radio', 'Радио кнопка'),
                         ('dropdown', 'Выпадающий список'),
                         ('date', 'Дата'),
                         ('checkbox', 'Чекбокс')]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=31, choices=FORM_TYPE_CHOICES)
    data = models.TextField(blank=True, null=True)  # Для radio, dropdown
    details = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Поле формы'
        verbose_name_plural = 'Поля форм'

    def __str__(self):
        return self.title


class FormBody(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    details = models.CharField(max_length=255, blank=True, null=True)
    form_fields = models.ManyToManyField(FormField)

    class Meta:
        default_related_name = 'form_bodies'
        verbose_name = 'Тело формы'
        verbose_name_plural = 'Тела форм'

    def __str__(self):
        return self.title


class FormButton(MPTTModel):
    title = models.CharField('Заголовок', max_length=255)
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children',
                            on_delete=models.CASCADE,

                            )
    form_body = models.OneToOneField(FormBody,
                                     null=True,
                                     blank=True,
                                     verbose_name="form_body",
                                     on_delete=models.CASCADE
                                     )

    class Meta:
        verbose_name = 'Кнопка с формами'
        verbose_name_plural = 'Кнопки с формами'

    def __str__(self):
        return self.title
