# Generated by Django 3.1 on 2020-10-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms_gui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersrequest',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл пользовательского запроса'),
        ),
    ]