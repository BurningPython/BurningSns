"""
Created on 2013年12月16日

@author: july
"""
from django import forms

from .models import User


class LoginForm(forms.Form):
    """
    """
    username = forms.CharField(label = "用户名", max_length = 30)
    password = forms.CharField(label = "密码", max_length = 30, min_length = 6, widget = forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    """
    """

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email')

    password = forms.CharField(label = "密码", max_length = 30, min_length = 6, widget = forms.PasswordInput())
    password2 = forms.CharField(label = "确认密码", max_length = 30, min_length = 6, widget = forms.PasswordInput())


    def clean_password2(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码输入不一致")


if __name__ == '__main__':
    pass
