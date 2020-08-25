from django.contrib import admin
from django.contrib.auth.models import User, Group
from django import forms

from forms_gui.models import FormBody, FormField, FormButton


class FormButtonForm(forms.ModelForm):
    class Meta:
        model = FormButton
        fields = ('title', 'parent', 'form_body')

    def clean(self):
        title = self.cleaned_data.get('title')
        parent = self.cleaned_data.get('parent')
        form_body = self.cleaned_data.get('form_body')

        if not title:
            if not form_body and not parent:
                raise forms.ValidationError(
                    'Должнен быть указан "Заголовок группы", либо "К какой группе относится", '
                    'либо "К какой справке ведет"'
                )
            if parent:
                raise forms.ValidationError(
                    'Если указано "К какой группе относится", должен быть указан '
                    'Заголовок группы'
                )
        return self.cleaned_data


class FormButtonAdmin(admin.ModelAdmin):
    form = FormButtonForm


admin.site.register(FormBody)
admin.site.register(FormField)
admin.site.register(FormButton, FormButtonAdmin)


admin.site.site_header = "Панель Администратора МФЦ"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Добро пожаловать в Панель Администратора МФЦ"

admin.site.index_template = "index.html"


admin.site.unregister(User)
admin.site.unregister(Group)
