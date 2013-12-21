'''
Created on 2013年12月16日

@author: july
'''
from Accounts.models import MyUser
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django import forms

class LoginForm(forms.Form):
    """
    """
    username = forms.CharField(label="用户名",max_length=30)
    password = forms.CharField(label="密码",max_length=30, min_length=6,widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    """
    """
    username = forms.CharField(label="用户名",max_length=30)
    email = forms.EmailField(label="Email",max_length=255)
    password = forms.CharField(label="密码",max_length=30, min_length=6,widget=forms.PasswordInput())
    password2 = forms.CharField(label="确认密码",max_length=30,min_length=6,widget=forms.PasswordInput())

    def clean_email(self):
        try:
            user = MyUser.objects.get(email = self.cleaned_data["email"])
        except ObjectDoesNotExist:
            return
        else:
            if user:
                raise ValidationError("该Email地址已经被使用")
            
if __name__ == '__main__':
    pass