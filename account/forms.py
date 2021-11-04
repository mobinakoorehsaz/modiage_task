from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


class UserCreateForm(forms.ModelForm):
    """
    add user
    """
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password2'] != data['password1']:
            raise forms.ValidationError('password not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    update user info
    """
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    """
    sing in form
    """
    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        fields = ['email', 'password', ]


class CheckboxForm(forms.Form):
    """
    permission page check box form
    """
    user = forms.ModelChoiceField(queryset=User.objects.exclude(is_admin=True))
    chart_1 = forms.BooleanField(required=False)
    chart_2 = forms.BooleanField(required=False)

    class Meta:
        fields = ['user', 'chart_1', 'chart_2', ]
