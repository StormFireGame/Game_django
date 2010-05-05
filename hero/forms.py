from django import forms
from django.forms.extras.widgets import SelectDateWidget

from hero.models import Hero

import re

class LoginForm(forms.Form):
#
    login = forms.CharField(label='Login', max_length=32)
    password = forms.CharField(label='Password', max_length=32,
                               widget=forms.PasswordInput())
    
class RegistrationForm(forms.Form): 
#
    login = forms.CharField(label='Login', max_length=32, min_length=3)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', max_length=32, min_length=5,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)', max_length=32,
                                widget=forms.PasswordInput())
    date_of_birthday = forms.DateField(label='Date of birthday',
                                       widget=SelectDateWidget(
                                                    years=range(1950, 2005)))
    SEXS = ((0, 'Male'), (1, 'Female'))
    sex = forms.IntegerField(widget=forms.RadioSelect(choices=SEXS))
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
#
        raise forms.ValidationError('Passwords do not match.')

    def clean_login(self):
        login = self.cleaned_data['login']
        if not re.search(r'^\w+$', login):
#
            raise forms.ValidationError('Login can only contain '
                                        'alphanumeric characters and' 
                                        ' the underscore.')
        try:
            Hero.objects.get(login=login)
        except Hero.DoesNotExist:
            return login
#
        raise forms.ValidationError('Login is already taken.')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Hero.objects.get(email=email)
        except Hero.DoesNotExist:
            return email
#
        raise forms.ValidationError('Email is already taken.')