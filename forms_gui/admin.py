from django.contrib import admin
from django.contrib.auth.models import User, Group
from django import forms

from forms_gui.forms import DynamicArrayField
from forms_gui.models import FormBody, FormField, FormButton, UsersRequest


class FormButtonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_body'].queryset = FormBody.objects.all().filter(form_button__isnull=True)

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
                    'Должен быть указан "Заголовок группы", либо "К какой группе относится", '
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


class FormFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ('title', 'type', 'data', 'details', 'required')
        field_classes = {
            'data': DynamicArrayField
        }

    class Media:
        js = ('forms_gui/js/dynamic_array.js',)


class FormFieldAdmin(admin.ModelAdmin):
    form = FormFieldForm
    change_form_template = 'admin/forms_gui/form_edit.html'

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.2.1.slim.min.js',
            'forms_gui/js/data_field_popup.js',
        )


class UsersRequestAdmin(admin.ModelAdmin):
    exclude = ('data',)


admin.site.register(FormBody)
admin.site.register(FormField, FormFieldAdmin)
admin.site.register(FormButton, FormButtonAdmin)
admin.site.register(UsersRequest, UsersRequestAdmin)

admin.site.site_header = "Панель Администратора МФЦ"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Добро пожаловать в Панель Администратора МФЦ"

admin.site.index_template = "index.html"

# admin.site.unregister(User)
# admin.site.unregister(Group)
