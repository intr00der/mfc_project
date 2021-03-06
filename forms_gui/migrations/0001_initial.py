# Generated by Django 3.1 on 2020-09-09 07:54

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('details', models.CharField(blank=True, max_length=255, null=True, verbose_name='Поясняющий текст для справки')),
            ],
            options={
                'verbose_name': 'Справка',
                'verbose_name_plural': 'Справки',
                'default_related_name': 'form_bodies',
            },
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название поля')),
                ('type', models.CharField(choices=[('text', 'Текст'), ('radio', 'Радио кнопки'), ('dropdown', 'Выпадающий список'), ('date', 'Поле даты'), ('checkbox', 'Чекбокс')], max_length=31, verbose_name='Тип поля')),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=31), blank=True, null=True, size=None)),
                ('details', models.CharField(blank=True, max_length=255, null=True, verbose_name='Поясняющий текст')),
                ('required', models.BooleanField(default=False, verbose_name='Обязательное ли поле')),
            ],
            options={
                'verbose_name': 'Поле справки',
                'verbose_name_plural': 'Поля справок',
            },
        ),
        migrations.CreateModel(
            name='UsersRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(verbose_name='Данные пользователя')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('form_body', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_request', to='forms_gui.formbody')),
            ],
        ),
        migrations.CreateModel(
            name='FormButton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок группы')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('form_body', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_button', to='forms_gui.formbody', verbose_name='К какой справке ведет')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='forms_gui.formbutton', verbose_name='К какой группе относится')),
            ],
            options={
                'verbose_name': 'Группа справки',
                'verbose_name_plural': 'Группы справок',
            },
        ),
        migrations.AddField(
            model_name='formbody',
            name='form_fields',
            field=models.ManyToManyField(related_name='form_body', to='forms_gui.FormField', verbose_name='Поля справки'),
        ),
    ]
