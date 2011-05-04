from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from main.forms import LoginForm, RegistrationForm
from hero.models import Hero

import hashlib

def main(request, template_name='main/main.html'):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                hero = Hero.objects.get(login=form.cleaned_data['login'],
                                        password=hashlib.sha1(
                                    form.cleaned_data['password']).hexdigest())
                request.session['hero_id'] = hero.id
                return HttpResponseRedirect(reverse('hero'))
            except Hero.DoesNotExist:
#
                messages.add_message(request, messages.ERROR,
                                     'Hero doesn\'t exist.')
    else:
        form = LoginForm()

    variables = RequestContext(request, {'form': form})

    return render_to_response(template_name, variables)

def registration(request, template_name='main/registration.html'):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            hero = Hero(login=form.cleaned_data['login'],
                        password=form.cleaned_data['password1'],
                        email=form.cleaned_data['email'],
                        sex = form.cleaned_data['sex'])
            hero.save()
            request.session['hero_id'] = hero.id
            return HttpResponseRedirect(reverse('hero'))
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form': form})

    return render_to_response(template_name, variables)
